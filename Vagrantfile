
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "bin/rootstrap.sh"
  config.vm.provision :shell, path: "bin/userstrap.sh", privileged: false
  config.vm.network "forwarded_port", guest: 8008, host: 8009
end
