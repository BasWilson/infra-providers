# Digitalocean
DigitalOcean provider for [Infra](https://github.com/baswilson/infra)

# Installation
## Requirements
- [Infra](https://github.com/baswilson/infra)

## install
```bash
infra provider install digitalocean
```

## Required environment variables
- DIGITALOCEAN_TOKEN - DigitalOcean API token

## Example in infra.yaml
```yaml
resources:
  - id: droplet
    provider: digitalocean
    type: droplet
    size: s-1vcpu-1gb
    image: ubuntu-20-04-x64
    backups: false
    ipv6: true
    monitoring: true
    region: ams3
```