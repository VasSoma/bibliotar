from datetime import datetime, timedelta
from sqlalchemy import select
from ...extensions import db
from ...models.loan import Loan
from ...models.fines import Fines

MAX_USER_EXTENSIONS = 2


class LoansService:
    @staticmethod
    def get_history(requester_id, requester_roles, user_id):
        try:
            role_names = [r["role_name"] for r in requester_roles]

            if "librarian" in role_names:
                loans = db.session.execute(select(Loan)).scalars().all()
            elif "user" in role_names:
                if requester_id != user_id:
                    return False, "Access denied"
                loans = db.session.execute(
                    select(Loan).filter_by(user_id=user_id)
                ).scalars().all()
            else:
                return False, "Access denied"

            result = []
            for loan in loans:
                result.append({
                    "loan_id": loan.loan_id,
                    "user_id": loan.user_id,
                    "book": {
                        "book_id": loan.book.book_id,
                        "title": loan.book.title,
                        "author": loan.book.author
                    },
                    "start_date": loan.start_date,
                    "due_date": loan.due_date,
                    "extension_count": loan.extension_count
                })

            return True, result
        except Exception as e:
            return False, f"Failed to get history: {e}"

    @staticmethod
    def extend_loan(requester_id, requester_roles, loan_id):
        try:
            role_names = [r["role_name"] for r in requester_roles]

            loan = db.session.execute(
                select(Loan).filter_by(loan_id=loan_id)
            ).scalar_one_or_none()

            if not loan:
                return False, "Loan not found"

            if "user" in role_names:
                if loan.user_id != requester_id:
                    return False, "Access denied"
                if loan.extension_count >= MAX_USER_EXTENSIONS:
                    return False, f"Maximum {MAX_USER_EXTENSIONS} extensions allowed"

            loan.due_date = loan.due_date + timedelta(days=7)
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
            role_names = [r["role_name"] for r in requester_roles]
            if "librarian" not in role_names:
                return False, "Only librarians can process returns"

            loan = db.session.execute(
                select(Loan).filter_by(loan_id=loan_id)
            ).scalar_one_or_none()

            if not loan:
                return False, "Loan not found"

            if loan.return_date:
                return False, "Loan already returned"

            loan.return_date = datetime.now()
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
            role_names = [r["role_name"] for r in requester_roles]
            if "librarian" not in role_names:
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
