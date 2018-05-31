# Database App
Die Anwendung startet einen Server, der Daten aus einer Datenbank abfragt und das Ergebnis über eine REST API verfügbar
macht. Zu jeder Datenmanipulation gibt es eine URL, in der automatisch die Daten per Javascript über
die API werden und anschließend eine Javascript Methode `processData` übergeben werden.

## Erezugen der Datenbank anhand der Quelldateien
1. Erstelle und starte eine *leere* Postgresql Datenbank und ändere die `main.conf` entsprechend.
2. Kopiere die Dateien  `transactions_input.csv`, `transactions_output.csv` und `transactions_blocks.csv`
in den Ordner `data`.
3. Führe `python db.py` aus.

## Datenmigration
### Head `transactions_input.csv`
#### transaction_id
0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5

#### inputs_input_script_string 
PUSHDATA(4)[ffff001d] PUSHDATA(1)[04]
PUSHDATA(4)[ffff001d] PUSHDATA(1)[0b]

#### inputs_input_sequence_number
4294967295
4294967295

#### inputs_input_pubkey_base58 (discard)
""
""

### timestamp
1231469665000
1231469744000

### Head `transactions_output.csv`
#### transaction_id
0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5

#### outputs_output_satoshis
5000000000
5000000000

#### outputs_output_script_string
PUSHDATA(65)[0496b538e853519c726a2c91e61ec11600ae1390813a627c66fb8be7947be63c52da7589379515d4e0a604f8141781e62294721166bf621e73a82cbf2342c858ee] CHECKSIG
PUSHDATA(65)[047211a824f55b505228e4c3d5194c1fcfaa15a456abdf37f9b9d97a4040afc073dee6c89064984f03385237d92167c13e236446b417ab79a0fcae412ae3316b77] CHECKSIG

#### outputs_output_pubkey_base58 (discard)

####timestamp
1231469665000
1231469744000



### Head `transactions_blocks.csv`
#### transaction_id
0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5

#### block_id
000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd
00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048

#### previous_block (discard)
000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048

#### merkle_root (discard)
0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
9b0fc92260312ce44e74ef369f5c66bbb85848f2eddd5a7a1cde251e54ccfdd5

#### nonce (discard)
2573394689
1639830024

#### version (discard)
1
1

#### timestamp
1231469665000
1231469744000

