# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell" do |s|
    s.inline = <<-SHELL
        set -euo pipefail
        IFS=$'\n\t'
        set +H
        sudo apt-get install python-software-properties
        if [ ! -f /etc/apt/sources.list.d/fkrull-deadsnakes-trusty.list ]
        then
            sudo apt-add-repository ppa:fkrull/deadsnakes
        fi
        if [ ! -f /etc/apt/sources.list.d/pgdg.list ]
        then
            sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
            wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        fi
        sudo apt-get update
        sudo apt-get install -y postgresql python3.5-complete
        sudo apt-get build-dep -y python3-psycopg2
        sudo -H python3.5 -m ensurepip
        sudo -H pip3.5 install --upgrade pip
        cd /vagrant
        sudo -H pip3.5 install -r requirements.txt
        if [ "$(sudo -u postgres psql -l | grep vagrant | head -n 1 | awk '{print $1}')" != "vagrant" ]
        then
            printf "Create DB vagrant with user vagrant"
            sudo -u postgres createdb vagrant
            set +e
            sudo -u postgres psql -c "create user vagrant with superuser password 'vagrant'"
            if [ $? -ne 0 ]
            then
                sudo -u postgres psql -c "alter user vagrant with superuser password 'vagrant'"
            fi
            set -e
            cp ./local_settings.templ.py ./local_settings.py
            sudo service postgresql restart
            python3.5 ./manage.py migrate
        fi
      SHELL
    s.privileged = false
  end
end
