from mpd import MPDClient

cli = MPDClient()

MPDClient.connect(cli, "localhost", 6600)

cli.status()
