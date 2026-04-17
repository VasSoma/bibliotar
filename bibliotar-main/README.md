# BiblioTár
A rendszerfejlesztés haladó módszerei kurzus keretein belül megvalósított projekt. Téma: BilbioTár.

## Hozzáférés beállítása terminálban

### Windows
**1. Érdemes Windows-on letölteni a Git Bash csomagot. Ennek használatával ugyanazok a parancsok használhatók, mint Linux-on.**
  https://git-scm.com/install/windows

**PowerShell**

**1. SSH Kulcs generálása**

*ssh-keygen -t ed25519 -C "email@example.com"*
  - Nyugodtan mentsétek a kulcsot az alapértelmezett könyvtárba.
  - Passphrase nem kell.

 **2. SSH kulcs kiíratása**
 
 type $env:USERPROFILE\.ssh\id_ed25519.pub
  - Ez kiíratja a nyilvános kulcsot, pl.: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... email@example.com
  - Az egész sort fel kell tölteni GitHub-ra

### Linux

**1. SSH kulcs generálása**
*ssh-keygen -t ed25519 -C "email@example.com"*

**2. SSH kulcs kiíratása**

*cat ~/.ssh/id_ed25519.pub*

### Windows + Linux

**3. SSH kulcs feltöltése GitHub-ra**
  - Profil kép (jobb felső sarok) → Settings
  - SSH and GPG keys
  - New SSH key
  - Címhez pl. a gép neve amit használsz
  - Key: ide kell bemásolni a kulcsot

**4. SSH kapcsolat tesztelése**
  - *ssh -T git@github.com*
  - Ha minden jó, a következő üzenetet írja ki: "Hi {username}! You've successfully authenticated, but GitHub does not provide shell access."

**5. Repo klónozása**

Ne felejtsétek átírni a *username* változót:

*git clone git@github.com:username/repository.git*
