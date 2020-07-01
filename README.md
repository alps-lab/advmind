# AdvMind

This is the code implementation (pytorch) for 2020 kdd paper: 
[AdvMind: Inferring Adversary Intent of Black-Box Attacks](https://arxiv.org/abs/2006.09539)

> Warning: The code will be migrated to our future project **Trojan-Zoo**. We will no longer maintain this repository. You can view the latest version at Trojan-Zoo in the future.

Quick Start:

1. Train a model:

   e.g. ResNetComp18 for CIFAR10 with 95% Acc
   

``` python3
   python train.py --verbose --save --batch_size 128
   ```

2. Test AdvMind:   

``` python3
   python advmind.py --verbose --pretrain --attack_adapt --defend_adapt --active --output 15
   ```

Usage:

1. python train.py --help
2. python advmind.py --help

Parameters Config: (Priority Increasing)

> The higher priority config will override lower priority ones.

1. Package Default: `/trojanzoo/config/`
    > You can use this as a template to set other configs.

2. Workspace Default: `/config/`
3. Custom Config: `--config [config location]`
4. CMD parameters: `--[parameter] [value]`
Output Verbose Information:

1. CMD arguments and modules: `--verbose`
2. AdvMind verbose information: `--output [number]`
