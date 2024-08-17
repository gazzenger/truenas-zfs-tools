## ZFS-Unlock-SSH

This tool is adapted to allow unlocking a Truenas ZFS dataset encrypted by a passphrase via SSH.

Ensure the user has already been configured for SSH access via public/private key pairs with the Truenas Instance.

This script has been adapted from the following sources,
* https://matouschek.org/blog/truenas-scale-unlock-from-cli/
* https://gist.github.com/mcdamo/ed7cdcaf51069cddd025b4bc1adf2250

The main purpose of this method is my preference to utilise CLI tooling rather than needing to perform HTTP requests to get the job done.

This tool takes an optional argument if you want to lock the datasets, i.e. ./zfs-unlock-ssh.sh lock

You must provide a .env file containing the following
#SSH_HOST=
#SSH_USER=
#datasets=()

When the command is run the datasets are looped over, and the passphrase is used for unlocking or locking the dataset.


