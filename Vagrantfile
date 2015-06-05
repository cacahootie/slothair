
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "bin/bootstrap.sh"
  config.vm.network "forwarded_port", guest: 6666, host: 6666
end
