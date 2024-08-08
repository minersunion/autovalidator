# AutoValidator

Whitehat bittensor validator initiative, the AutoValidator aim to facilitate validation process across all subnets.

# How to use

```bash
python core/generate_config.py

> Enter the project name: 
> Enter the GitHub repository URL: 
> Enter the deployment path on the server: 
> Enter the Python version to use: 
> Do you need to add an API key? (yes/no): 
> Inventory generated: inventories/dev/hosts.yml
> Group vars file generated: inventories/dev/group_vars/
> Playbook generated: playbooks/deploy_
> Role generated: roles/role_
```

## Ansible

> Make sure you have SSH access to the servers defined in your inventory. You should be able to SSH into them without requiring a password (using SSH keys)

Deploy
```sh
ansible-playbook -i inventories/testnet/hosts.yml playbooks/deploy_text-prompting.yml -vvv
```

Check changes
```sh
ansible-playbook -i inventories/testnet/hosts.yml playbooks/deploy_text-prompting.yml -vvv --check
```

## KPIs for any subnet owner

- [wip - ddos](docs/ddos.md)
- [wip - min_compute](docs/min_compute.md)
- [wip - relay mining](docs/relay_mining.md)
- [weights copying](docs/weights_copying.md)

This list is non-exhaustive. 
