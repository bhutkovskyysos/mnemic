$script = <<SCRIPT
sudo apt update
sudo apt install python3-pip -y
sudo pip3 install nose
sudo pip3 install jupyter
sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install matplotlib 
sudo pip3 install ipython 
sudo pip3 install pandas
sudo apt-get install zip unzip -y
sudo pip3 install sqlalchemy==1.3.23
sudo apt-get install dos2unix
sudo apt-get install libpq-dev python-dev -y
sudo pip3 install psycopg2
sudo pip3 install asyncpg
sudo apt install python3-sklearn -y
sudo pip3 install seaborn
sudo pip3 install --upgrade tensorflow
sudo pip3 install aiohttp
sudo pip3 install ipywidgets
sudo pip3 pip install -U sphinx
sudo pip3 install sphinx-rtd-theme
sudo echo 'alias psql="docker exec -it my-db psql -U postgres"' >> /home/vagrant/.bashrc
sudo echo 'alias dropdb="docker exec -it my-db dropdb -U postgres"' >> /home/vagrant/.bashrc
sudo echo 'alias createdb="docker exec -it my-db createdb -U postgres"' >> /home/vagrant/.bashrc
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"

  # require plugin https://github.com/leighmcculloch/vagrant-docker-compose
  config.vagrant.plugins = "vagrant-docker-compose"

  # install docker and docker-compose
  config.vm.provision :docker
  config.vm.provision :docker_compose

  config.vm.provision "shell", inline: $script

     for i in 8888..8900
        config.vm.network :forwarded_port, guest: i, host: i-2000
     end

  config.vm.network "forwarded_port", guest: 12012, host: 12012, protocol: "udp"
  config.vm.provider "virtualbox" do |vb|
      vb.memory = "2000"
      vb.name = "mnemic"
  end

end

