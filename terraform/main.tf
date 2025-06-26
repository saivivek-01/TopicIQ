terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_ssh_key" "default" {
  name       = "topiciq-key"
  public_key = file("~/.ssh/topiciq_rsa.pub")
}

resource "digitalocean_droplet" "web" {
  image              = "docker-20-04"
  name               = "topiciq-droplet"
  region             = "nyc3"
  size               = "s-1vcpu-1gb"
  ssh_keys           = [digitalocean_ssh_key.default.id]
  backups            = false
  ipv6               = true
  monitoring         = true
  tags               = ["web"]
}

output "droplet_ip" {
  value = digitalocean_droplet.web.ipv4_address
}