---
title: "Installing Linux on Mi Notebook Pro 14"
date: 2023-03-31T16:18:40+05:30
draft: true
---

I had a horrible time trying to setup Linux on my Mi Notebook Pro. The USB boot is pretty much unusable.
The UEFI interface configuration lets you enable USB boot, but shows no options for it in the boot order.

Even if you use windows recovery to try to boot to USB, the UEFI check aborts the operation halfway, saying
that you need to set it in the boot order menu.

To workaround this, I had to install an EFI bootloader that would let me boot to USB. For reference. ((add more information about UEFI/BIOS)).
I chose refined, since that is the one EFI bootloader I'm familiar with. Had to manually copy efi files to the EFI parition on windows cmdline.

once that all was over, I was able to boot USB, by leveraging refind's ability to find other bootloaders.

hey xiaomi & microsoft, if you guys are reading this, please make it easier for people to boot linux. love!