new rl(`rho:registry:lookup`), deployId(`rho:rchain:deployId`), RevVaultCh, vaultCh, balanceCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$addr", *vaultCh) |
    for (@(true, vault) <- vaultCh) {
      @vault!("balance", *balanceCh) |
      for (@balance <- balanceCh) {
        deployId!(balance)
      }
    }
  }
}
