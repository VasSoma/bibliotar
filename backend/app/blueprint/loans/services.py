from datetime import datetime, timedelta, timezone

from apiflask import HTTPError
from sqlalchemy import select, or_

from ...models.users import User
from ..auth.services import AuthService
from ..books.service import BookService
from ...extensions import db
from ...models.loan import Loan
from ...models.book import Book
from ...models.fines import Fines

DAILY_FINE_AMOUNT = 1

MAX_USER_EXTENSIONS = 2
USER_EXTENSION_DAYS = 1
LIBRARIAN_EXTENSION_DAYS = 7


class LoansService:

    @staticmethod
    def get_loans(requester_id, requester_roles, search):
        role = list(reversed(requester_roles))[0]

        query = select(Loan).join(Loan.book).join(Loan.user)

        if role["role_name"] == "user":
            query = query.where(Loan.user_id == requester_id)

        if search:
            pattern = f"%{search}%"
            conditions = [
                Book.title.ilike(pattern),
                Book.author.ilike(pattern),
            ]

            if role["role_name"] == "librarian" or role["role_name"] == "admin":
                conditions.append(User.name.ilike(pattern))

            query = query.where(or_(*conditions))

        loans = db.session.execute(query).scalars().all()
        result = []
        for loan in loans:
            if loan.return_date:
                overdue_fine = None
            else:
                overdue_days = max(0, (datetime.now() - loan.due_date).days)
                overdue_fine = (
                    overdue_days * DAILY_FINE_AMOUNT if overdue_days > 0 else None
                )

            result.append(
                {
                    "loan_id": loan.loan_id,
                    "user_id": loan.user_id,
                    "book": {
                        "book_id": loan.book.book_id,
                        "title": loan.book.title,
                        "author": loan.book.author,
                    },
                    "start_date": loan.start_date,
                    "due_date": loan.due_date,
                    "return_date": loan.return_date,
                    "extension_count": loan.extension_count,
                    "overdue_fine": overdue_fine,
                }
            )
        return True, result

    @staticmethod
    def get_loan(requester_id, requester_roles, loan_id):
        role = list(reversed(requester_roles))[0]

        query = select(Loan).where(Loan.loan_id == loan_id)

        if role["role_name"] == "user":
            query = query.where(Loan.user_id == requester_id)

        loan = db.session.execute(query).scalar_one_or_none()

        if not loan:
            return False, "Loan not found"

        end_date = loan.return_date or datetime.now()
        overdue_days = max(0, (end_date - loan.due_date).days)
        overdue_fine = overdue_days * DAILY_FINE_AMOUNT

        return True,  {
            "loan_id": loan.loan_id,
            "user_id": loan.user_id,
            "book": {
                "book_id": loan.book.book_id,
                "title": loan.book.title,
                "author": loan.book.author,
            },
            "start_date": loan.start_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "extension_count": loan.extension_count,
            "overdue_fine": overdue_fine,
        }


    @staticmethod
    def extend_loan(requester_id, requester_roles, loan_id):
        try:
            role = list(reversed(requester_roles))[0]

            loan = db.session.execute(
                select(Loan).filter_by(loan_id=loan_id)
            ).scalar_one_or_none()

            if not loan:
                return False, "Loan not found"

            if role["role_name"] == "librarian":
                extension_days = LIBRARIAN_EXTENSION_DAYS
            elif role["role_name"] == "user":
                if loan.user_id != requester_id:
                    return False, "Access denied"
                if loan.extension_count >= MAX_USER_EXTENSIONS:
                    return False, f"Maximum {MAX_USER_EXTENSIONS} extensions allowed"
                extension_days = USER_EXTENSION_DAYS
            else:
                return False, "Access denied"

            loan.due_date = loan.due_date + timedelta(days=extension_days)
            loan.extension_count += 1
            db.session.commit()

            return True, {
                "loan_id": loan.loan_id,
                "due_date": loan.due_date,
                "extension_count": loan.extension_count
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to extend loan: {e}"

    @staticmethod
    def return_loan(requester_roles, loan_id):
        try:
            role = list(reversed(requester_roles))[0]

            if role["role_name"] == "librarian":
                return False, "Only librarians can process returns"

            loan = db.session.execute(
                select(Loan).filter_by(loan_id=loan_id)
            ).scalar_one_or_none()

            if not loan:
                return False, "Loan not found"

            if loan.return_date:
                return False, "Loan already returned"

            loan.return_date = datetime.now()

            overdue_days = max(0, (loan.return_date - loan.due_date).days)
            if overdue_days > 0:
                fine = db.session.execute(
                    select(Fines).filter_by(loan_id=loan_id, is_paid=False)
                ).scalar_one_or_none()
                if fine:
                    fine.amount = overdue_days * DAILY_FINE_AMOUNT
                else:
                    fine = Fines(
                        loan_id=loan.loan_id,
                        user_id=loan.user_id,
                        amount=overdue_days * DAILY_FINE_AMOUNT,
                        is_paid=False
                    )
                    db.session.add(fine)

            db.session.commit()

            return True, {
                "loan_id": loan.loan_id,
                "return_date": loan.return_date
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to process return: {e}"

    @staticmethod
    def fine_paid(requester_roles, loan_id):
        try:
            role = list(reversed(requester_roles))[0]
            if role["role_name"] != "librarian":
                return False, "Only librarians can mark fines as paid"

            fine = db.session.execute(
                select(Fines).filter_by(loan_id=loan_id, is_paid=False)
            ).scalar_one_or_none()

            if not fine:
                return False, "No unpaid fine found for this loan"

            fine.is_paid = True
            db.session.commit()

            return True, {
                "fine_id": fine.fine_id,
                "loan_id": fine.loan_id,
                "amount": fine.amount,
                "is_paid": fine.is_paid
            }
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to mark fine as paid: {e}"

    @staticmethod
    def create_loan(json_data, requester_id, requester_roles):
        book = BookService.get_book_by_id(json_data["book_id"])
        current_user = AuthService.get_current_user()
        current_user_roles = AuthService.get_roles_by_user_id(current_user.user_id)
        role = list(reversed(requester_roles))[0]

        if role["role_name"] == "user" and json_data["user_id"] != requester_id:
            raise HTTPError(403, "Users can only create loans for themselves.")
        else:
            user = User.query.get(json_data["user_id"])
            if not user:
                raise HTTPError(404, "User not found.")

        if not book:
            raise HTTPError(404, "Book does not exist.")
        elif not book.is_available:
            raise HTTPError(404, "Book is not available.")
        else:
            now = datetime.now(timezone.utc)

            loan = Loan(
                user_id = json_data["user_id"],
                book_id = json_data["book_id"],
                start_date = now,
                due_date = now + timedelta(days=7),
                return_date = None,
                extension_count = 0
            )

            if book.quantity > 0:
                book.quantity -= 1

            if book.quantity == 0:
                book.is_available = False   

            db.session.add(loan)
            db.session.commit()

        return loan
