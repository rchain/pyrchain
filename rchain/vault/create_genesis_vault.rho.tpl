new rl(`rho:registry:lookup`), RevVaultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreateGenesisVault", "$addr", $balance, Nil)
  }
}
