# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.network "private_network", ip: "192.168.50.4"
  config.vm.define "ubuntutest" do |ubuntutest|
    ubuntutest.vm.hostname = "ubuntu-server"
    ubuntutest.vm.box = "trusty-server"
    ubuntutest.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"
  end
  config.vm.synced_folder ".", "/vagrant/app"
end