import os


def prompt_for_api_keys():
    api_keys = {}
    while True:
        need_api_key = input("Do you need to add an API key? (yes/no): ").strip().lower()
        if need_api_key == "yes":
            api_name = input("API Key name: ").strip()
            api_value = input(f"Value for {api_name}: ").strip()
            api_keys[api_name] = api_value
        elif need_api_key == "no":
            break
        else:
            print("Please answer 'yes' or 'no'.")
    return api_keys


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_inventory(project_name):
    inventory_dir = f"inventories/testnet"
    create_directory(inventory_dir)

    inventory_content = f"""all:
  children:
    {project_name}:
      hosts:
        serveur1:
        serveur2:
    """
    inventory_file = os.path.join(inventory_dir, "hosts.yml")

    with open(inventory_file, "w") as file:
        file.write(inventory_content.strip())

    print(f"Inventory generated: {inventory_file}")


def generate_group_vars(project_name, repo_url, deploy_path, python_version, api_keys):
    group_vars_dir = f"inventories/testnet/group_vars"
    create_directory(group_vars_dir)

    config_content = f"""
repo_url: "{repo_url}"
deploy_path: "{deploy_path}"
python_version: "{python_version}"
    """

    if api_keys:
        config_content += "\napi_keys:\n"
        for name, value in api_keys.items():
            config_content += f'  {name}: "{value}"\n'

    config_file = os.path.join(group_vars_dir, f"{project_name}.yml")

    with open(config_file, "w") as file:
        file.write(config_content.strip())

    print(f"Group vars file generated: {config_file}")


def generate_playbook(project_name):
    playbooks_dir = "playbooks"
    create_directory(playbooks_dir)

    playbook_content = f"""---
- name: Deploy {project_name}
  hosts: {project_name}
  vars_files:
    - ../inventories/testnet/group_vars/{project_name}.yml
  roles:
    - role_{project_name}
    """

    playbook_file = os.path.join(playbooks_dir, f"deploy_{project_name}.yml")

    with open(playbook_file, "w") as file:
        file.write(playbook_content.strip())

    print(f"Playbook generated: {playbook_file}")


def generate_role(project_name):
    roles_dir = os.path.join("roles", f"role_{project_name}")
    create_directory(roles_dir)

    # Create subdirectories for the role
    subdirs = ["tasks", "templates", "handlers", "files", "vars"]
    for subdir in subdirs:
        create_directory(os.path.join(roles_dir, subdir))

    # Create main.yml in tasks and handlers
    tasks_content = """---
- name: Clone the repository
  git:
    repo: "{{ repo_url }}"
    dest: "{{ deploy_path }}"
    version: "main"
    update: yes

- name: Create Python virtual environment
  command: python{{ python_version }} -m venv {{ deploy_path }}/venv

- name: Install dependencies
  pip:
    requirements: "{{ deploy_path }}/requirements.txt"
    virtualenv: "{{ deploy_path }}/venv"

- name: Apply configuration template
  template:
    src: config_template.j2
    dest: /etc/{project_name}/config.conf
  notify:
    - Restart {project_name} service
    """

    handlers_content = f"""---
- name: Restart {project_name} service
  service:
    name: {project_name}
    state: restarted
    """

    # Write to main.yml in tasks and handlers
    with open(os.path.join(roles_dir, "tasks", "main.yml"), "w") as file:
        file.write(tasks_content.strip())

    with open(os.path.join(roles_dir, "handlers", "main.yml"), "w") as file:
        file.write(handlers_content.strip())

    # Create a config template in templates
    template_content = """# Configuration for {{ project_name }}

[app]
repo_url = {{ repo_url }}
deploy_path = {{ deploy_path }}
python_version = {{ python_version }}

{% if api_keys %}
[api_keys]
{% for key, value in api_keys.items() %}
{{ key }} = {{ value }}
{% endfor %}
{% endif %}

[server]
host = {{ ansible_host }}
port = {{ server_port | default(8000) }}

[database]
db_name = {{ db_name | default(project_name ~ '_db') }}
db_user = {{ db_user | default('user') }}
db_password = {{ db_password | default('password') }}
db_host = {{ db_host | default('localhost') }}
db_port = {{ db_port | default(5432) }}

[logging]
log_level = {{ log_level | default('INFO') }}
log_file = {{ log_file | default('/var/log/' ~ project_name ~ '.log') }}
    """

    with open(os.path.join(roles_dir, "templates", "config_template.j2"), "w") as file:
        file.write(template_content.strip())

    print(f"Role generated: {roles_dir}")


if __name__ == "__main__":
    project_name = input("Enter the project name: ").strip()
    repo_url = input("Enter the GitHub repository URL: ").strip()
    deploy_path = input("Enter the deployment path on the server: ").strip()
    python_version = input("Enter the Python version to use: ").strip()

    # Ask for API keys if needed
    api_keys = prompt_for_api_keys()

    # Generate the necessary files
    generate_inventory(project_name)
    generate_group_vars(project_name, repo_url, deploy_path, python_version, api_keys)
    generate_playbook(project_name)
    generate_role(project_name)
