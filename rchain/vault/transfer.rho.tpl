new rl(`rho:registry:lookup`), RevVaultCh, vaultCh, revVaultKeyCh, resultCh in {
  rl!(`rho:rchain:revVault`, *RevVaultCh) |
  for (@(_, RevVault) <- RevVaultCh) {
    @RevVault!("findOrCreate", "$from", *vaultCh) |
    @RevVault!("deployerAuthKey", *revVaultKeyCh) |
    for (@(true, vault) <- vaultCh; key <- revVaultKeyCh) {
      @vault!("transfer", "$to", $amount, *key, *resultCh) |
      for (_ <- resultCh) { Nil }
    }
  }
}
