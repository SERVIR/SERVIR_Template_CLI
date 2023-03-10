import fileinput
import os
import random
import shutil
import sqlite3
import stat
import string
import subprocess
import sys
import json
import click
import uuid

import git


@click.group()
def cli():
    pass


@cli.command()
@click.option('-n', '--name', type=str, help='New app name', default='my_application')
def create(name):
    click.echo(f"Creating template project {name}")
    process = subprocess.Popen(["django-admin", "startproject", f"{name}"],
                               shell=os.name == 'nt',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    if stderr:
        print(stderr)
    if stdout:
        print(stdout)

    temp_dir = str(uuid.uuid1())

    git.Git(os.path.join(os.getcwd(), temp_dir)).clone("git@github.com:SERVIR/AppTemplate2022.git",
                                                     os.path.join(os.getcwd(), temp_dir))

    source = os.path.join(os.getcwd(), temp_dir)
    target = os.path.join(os.getcwd(), f"{name}")

    shutil.copytree(source, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git*", "manage.py"))
    shutil.copyfile(os.path.join(
        target,
        "SERVIR_AppTemplate", "settings.py")
        , os.path.join(target, f"{name}", "settings.py"))
    shutil.copyfile(os.path.join(
        target,
        "SERVIR_AppTemplate", "urls.py")
        , os.path.join(target, f"{name}", "urls.py"))

    replace_string_in_file(os.path.join(target, f"{name}"), name, "settings.py", "SERVIR_AppTemplate")
    try:
        replace_string_in_file(target, name, "environment.yml", "SERVIR_AppTemplate")
    except Exception as e:
        click.echo(str(e))

    letters = string.ascii_letters + string.digits + string.punctuation
    letters = letters.replace("/", "").replace("\\", "").replace("\"", "").replace("'", "")
    result_str = ''.join(random.choice(letters) for i in range(64))

    with open(os.path.join(os.path.dirname(__file__), "support", "data.json"), 'r+') as f:
        data = json.load(f)
        data["SECRET_KEY"] = result_str

    with open(os.path.join(target,"data.json"), 'w') as fs:
        json.dump(data, fs , indent=4, sort_keys=True)

    try:
        click.echo(f"Creating your conda environment named {name}, this may take some time, please wait.")
        process = subprocess.Popen(["conda", "env", "create", "-f", os.path.join(target, "environment.yml")],
                                   shell=os.name == 'nt',
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        for line in iter(process.stdout.readline, ''):
            line = line.replace('\r', '').replace('\n', '')
            click.echo(line)
            sys.stdout.flush()
        stdout, stderr = process.communicate()
        click.echo(str(stderr))
    except Exception as e2:
        click.echo(str(e2))

    activate_cmd = f"conda activate {name}"
    migrate_cmd = "python " + os.path.join(target, "manage.py") + " migrate"

    if os.name == 'nt':
        subprocess.call(activate_cmd +
                        " && " + migrate_cmd, shell=True)
    else:
        process = subprocess.Popen(["which conda"],
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)

        stdout, stderr = process.communicate()

        conda_path = os.path.join(os.path.split(os.path.split(stdout)[0])[0], "etc", "profile.d", "conda.sh")

        init_conda = 'source ' + conda_path

        subprocess.call(init_conda + " && " + activate_cmd +
                        " && " + migrate_cmd, executable='/bin/bash', shell=True)


    conn = sqlite3.connect(os.path.join(target, "db.sqlite3"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM django_site where id = 3")
    if len(cursor.fetchall()) == 1:
        cursor.execute('''UPDATE django_site 
        SET name = "127.0.0.1:8000", domain = "127.0.0.1:8000" 
        where id = 3;''')
    else:
        cursor.execute('''insert into django_site (id, name, "domain") 
        values (3, "127.0.0.1:8000", "127.0.0.1:8000");''')
    conn.commit()
    conn.close()

    # replace_string_in_file(target, result_str, "data.json", "SECRET_KEY_HOLDER")

    shutil.rmtree(os.path.join(target, "SERVIR_AppTemplate"))
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            os.chmod(os.path.join(root, directory), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(source)
    remove_file(os.path.join(target, "environment.yml.bak"))
    remove_file(os.path.join(target, f"{name}", "settings.py.bak"))


def remove_file(which):
    try:
        os.remove(which)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def replace_string_in_file(where, app_name, file_name, default_string):
    with fileinput.FileInput(os.path.join(where, file_name), inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(default_string, f"{app_name}"), end='')
