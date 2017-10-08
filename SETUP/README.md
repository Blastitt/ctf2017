Challenge Explanation & Setup Instructions
==========================================

**WARNING:** Spoilers. If you would rather try out
this challenge on your own first, DO NOT read past
this paragraph. Just place the directory containing
this challenge on an environment with 
[GnuPG](https://gnupg.org/), read the `README.md`
file located on the root directory containing this
challenge, and hack away.

## Requirements

Due to the nature of this challenge, the following
will be needed in order to successfully complete
this challenge:

- [GnuPG](https://gnupg.org/) (Any version, doesn't
matter)
- Common sense
- Resilience and patience while reading manpages
- The ability to read manpages

## Setup

Place the directory containing this challenge on
a Linux environment with GnuPG installed.

Ensure all challenge directories and files exist:

- attachments/
- emails/
- pub_keys/
- README.md

### Planting the "flag"

This challenge is designed to contain the "flag"
within an email message. Because the contents of
the email message MUST be pgp encrypted, you will
have to 1) decrypt the message 2) paste the flag
hash as part of the message, and 3) re-encrypt
the message with the correct public key.

The following steps will walk you through the
entirety of this process:

1. You will need to load Bob's private key
using gpg (preferably on your own machine, not
a competition box) in order to decrypt the
message.

A copy of Bob's private key has been provided
in the DEBUG directory. To load it simply execute
the command below:

```sh
$ gpg --import ./path/to/bob_private.asc
```

The key with id `A9487844` should now be
available in your gpg keyring. You can verify this
with:

```sh
$ gpg -k | grep A9487844
pub   2048R/A9487844 <date>
```

2. You will also need to load Bob's public key
to the gpg keyring. It should be available to
you and all competitors in the `./pub_keys`
directory:

```sh
gpg --import ./pub_keys/bob_public.asc
```

Note: this step may not be necessary, as the public
key should have been re-created and imported when
the private key was imported.

3. With Bob's private key in your keyring, locate
the file 
`./emails/bob_inbox/MSG_03_reply_from_alice.eml`

4. Upon reading it, you will notice that the
email headers at the top of the file are NOT
pgp encrypted, but just the body of the message.
It is important to leave the headers un-encrypted
when re-encrypting the message after planting the
flag.

3. Using `gpg`, perform the following command:

```sh
gpg --decrypt emails/bob_inbox/MSG_03_reply_from_alice.eml | sed -e s/PASTE_CHALLENGE_FLAG_HERE/<FLAG_HASH_FOR_THIS_CHALLENGE>/
```

4. The previous step should render the contents 
of the email in plaintext (minus the email headers), 
as well as a section at the end of the message 
beginning with 
`----------[FLAG]----------`. The hash should now be
present in this section. Redirect this output into
a file of its own, or into your clipboard.

Remove the gpg headers from the decrypted output
received from this step, leaving everything else
starting with `Bob,`:

```sh
$ gpg --encrypt -a --recipient bob@totallyineptsecurity.com decrypted_msg_with_flag_from_step_4.txt
```

Redirect the output from the command above to your
clipboard (or use the `--output` flag with the 
`gpg` command to specify a particular file to save to).

5. Then, leaving the email headers in the original
email file to Bob 
(`emails/bob_inbox/MSG_03_reply_from_alice.eml`) intact, 
replace the PGP encrypted section with the modified
encrypted message from `step 4`, now containing the flag.

6. Verify the contents of the modified email message
by executing:

```sh
$ gpg --decrypt emails/bob_inbox/MSG_03_reply_from_alice.eml
```

The output from the command above should now contain
the original message with the newly added flag at the end.

## Challenge Explanation 

Alice and Bob are good at their jobs as security engineers
at TotallyIneptSecurity, inc. They never try to come up with
their own encryption standards or implement untested
encryption algorithms, rather they use well-tested and
documented libraries for encrypting or hashing any
sensitive information they come across while on the job
and in their personal lives.

Alice and Bob ensure that every message they send is PGP
encrypted. Because of this, the only vulnerabilities one
might find in their methods are those inadvertedly created
by the weakest link in their company -- the sys admin.

The systems administrator at TotallyIneptSecurity has
recently developed an obsession with auditability. 
This obsession has extended to include "emergency access"
to any and all records created by the company's employees
including their private email conversations as well as
email attachments. As part of his new campaign to make
all the things auditable, the sys admin has created and
deployed a new email server to be used company-wide that
ensures "transparency" and "auditability".

One might even come to think of the sys admin as a sort
of "open source" evangelist, but you know,  for morons.

His new auditability policy collects and "securely"
stores all employee's gpg private keys in a single
central location - only accessible by the sys admin
himself of course.

He uses a program called `Cryptonite` (really just a
glorified Python script) to obfuscate keys before they
are sent to him via email by all employees of the
company.

By looking through the actual source code of the 
`Cryptonite` script, one discovers that the entire premise 
of the script is to XOR a victim's private key with his
public key - such that the operation can only be reversed
by himself and himself only (and everyone else ever, for 
that matter).

The challenge comes about a contestant reading plaintext
conversations between the sys admin and Alice and Bob,
and figuring out that both of their private keys (which
are obviously still present in the ever-persistent email
attachments folder) can be de-obfuscated and imported
into a gpg keychain in order to --decrypt all of the
messages on the server sent between Alice and Bob.

The flag hash will be located at the end of one of these
messages.

The contestant will be given hints that gpg was used as
part of email message-encryption through the README
available on the root directory containing this challenge.

The contestant must figure out (either through reading the
gpg manpage - or through online access if any) how to
import keys, as well as decrypt messages using imported
keys on the gpg keychain.

## Solution

To solve this challenge, a contestant must:

- Obtain Alice and Bob's obfuscated private keys from the
email `attachments` directory.
- De-obfuscate the keys using the `cryptonite.py` script
also conveniently located in the `attachments` directory.
They will have to figure out to feed the script both an
obfuscated private key and the sys admin's public GPG key, 
along with the `--decode` flag.
- Import the now-de-obfuscated private keys into the
gpg keychain on the machine containing this challenge.
- Use gpg to decrypt any messages addressed to Bob or Alice
with the now available private keys.

## Notes

**REMINDER:** TotallyIneptSecurity, inc reminds you
to kindly delete or remove this `DEBUG` directory
prior to making it available at your Capture The
Flag competition. And remember, "The best security
is the kind you can easily audit".
