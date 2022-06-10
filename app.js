const express = require('express')
const Web3 = require('web3')
var Tx = require("ethereumjs-tx").Transaction;
const CryptoJS = require('crypto-js');
const crypto = require("crypto")
const app = express()
var cors = require('cors')
// const JSEncrypt = require('jsencrypt');
const NodeRSA = require('node-rsa');
const key = new NodeRSA({b: 1024});
key.setOptions({
  encryptionScheme: "pkcs1"
});
const port = 3000

const abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			}
		],
		"name": "approve_access",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "access_type",
				"type": "uint256"
			}
		],
		"name": "init_priviledges",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "init_priviledges_admin",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "para",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "access_type",
				"type": "uint256"
			}
		],
		"name": "modify_priviledges",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "padd",
				"type": "address"
			}
		],
		"name": "request_access",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			}
		],
		"name": "revoke_access",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_owner",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "para",
				"type": "uint256[]"
			},
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "newPara",
				"type": "string[]"
			}
		],
		"name": "write_all_records",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "para",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "padd",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "newPara",
				"type": "string"
			}
		],
		"name": "write_record",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "accessAuthority",
		"outputs": [
			{
				"internalType": "address",
				"name": "doctor_address",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "patient_address",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "access",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "accessPriviledges",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "account_type",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "account_addr",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "add",
				"type": "address"
			}
		],
		"name": "list_account_priviledges",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256[10]",
				"name": "",
				"type": "uint256[10]"
			},
			{
				"internalType": "uint256[10]",
				"name": "",
				"type": "uint256[10]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "list_all_patients",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "list_priviledges",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256[10]",
				"name": "",
				"type": "uint256[10]"
			},
			{
				"internalType": "uint256[10]",
				"name": "",
				"type": "uint256[10]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			}
		],
		"name": "read_all_records",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "pid",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "para",
				"type": "uint256"
			}
		],
		"name": "read_record",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "records",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
];

app.use(cors())

app.use(express.json())

var smart_contract_addr = "0x279395A8DB4656e043319F075b08e7CC2dd3e66e";
var account_addr = "0x3738311e29EA5B33092063E5Eb8D43AD83012E07";
var account_private = Buffer.from('500ed35d98ee5e19dccb37699260b6b9c4225ef8e2902d344e95aaff0ec1d3bb', 'hex');

app.post('/api/getRecords', (req, res) => {

  var patient_dataset = [
    [
      Object({                                    // ADMISSIONS
        healthcare_admit_id: '123456',
        admit_time: '23-10-2164 21:09',
        discharge_time: '01-11-2164 17:15',
        admission_type: 'EMERGENCY',
        admission_location: 'EMERGENCY ROOM',
        discharge_location: 'HOME HEALTH CARE',
        insurance: 'Medicare',
        marital_status: 'Seperated',
        ethinicity: 'BLACK/AFRICAN',
        diagnosis: 'SEPSIS'
      }),
      Object({                                    // PATIENTS
        healthcare_admit_id: '123456',
        gender: 'F',
        dob: '2094-03-05 00:00:00',
        dod_hosp: '2165-08-12 00:00:00',
        expire_flag: '1'
      }),
      Object({                                    // CPTEVENTS
        healthcare_admit_id: '123456',
        ticket_id: '1',
        cost_center: 'ICU',
        section_header: 'Evaluation and management',
        subsection_header: 'Consultations',
      }),
      Object({                                    // LABEVENTS
        healthcare_admit_id: '123456',
        charttime: '2164-09-24 20:21:00',
        value: '19',
        valuenum: '19',
        valueuom: 'mEq/L',
        flag: ''
      }),
      Object({                                    // PATIENT ICD EVENTS
        healthcare_admit_id: '123456',
        icd9_code: '01716',
        short_title: 'Erythem nod tb-oth test',
        long_title: 'Erythema nodosum with hypersensitivity reaction in tuberculosis, tubercle bacilli not found by bacteriological or histological examination, but tuberculosis confirmed by other methods [inoculation of animals]'
      }),
      Object({                                    // INSURANCE
        healthcare_admit_id: '123456',
        claim_id: '35256',
        policy_id: '234',
        policy_limit: '100000',
        policy_expiry: '2169-09-24 20:19:00',
      })
    ],
    [
      Object({                                    // ADMISSIONS
        healthcare_admit_id: '568426',
        admit_time: '23-10-2162 21:09',
        discharge_time: '01-11-2162 17:15',
        admission_type: 'EMERGENCY',
        admission_location: 'EMERGENCY ROOM',
        discharge_location: 'HOME HEALTH CARE',
        insurance: 'Medicare',
        marital_status: 'Seperated',
        ethinicity: 'WHITE',
        diagnosis: 'HUMERAL FRACTURE'
      }),
      Object({                                    // PATIENTS
        healthcare_admit_id: '568426',
        gender: 'M',
        dob: '2097-03-05 00:00:00',
        dod_hosp: '2167-08-12 00:00:00',
        expire_flag: '1'
      }),
      Object({                                    // CPTEVENTS
        healthcare_admit_id: '568426',
        ticket_id: '1',
        cost_center: 'ICU',
        section_header: 'Radiology',
        subsection_header: 'Diagnostic ultrasound',
      }),
      Object({                                    // LABEVENTS
        healthcare_admit_id: '568426',
        charttime: '2164-09-24 20:21:00',
        value: '15',
        valuenum: '15',
        valueuom: 'mEq/L',
        flag: ''
      }),
      Object({                                    // PATIENT ICD EVENTS
        healthcare_admit_id: '568426',
        icd9_code: '01716',
        short_title: 'Erythem nod tb-oth test',
        long_title: 'Erythema nodosum with hypersensitivity reaction in tuberculosis, tubercle bacilli not found by bacteriological or histological examination, but tuberculosis confirmed by other methods [inoculation of animals]'
      }),
      Object({                                    // INSURANCE
        healthcare_admit_id: '568426',
        claim_id: '35258',
        policy_id: '356',
        policy_limit: '200000',
        policy_expiry: '2169-09-24 20:19:00',
      })
    ]
  ];
  
  // column_names: string[];
  // values: string[];
  // json_encoded: string;
  // encrypted_data: string;
  // decrypted_data: string;
  // blockchain_data!: string;
  // blockchain_decrypted!: string;
  var nonce_value;
  // loading: boolean = false; 

  // var Web3 = require('web3/dist/web3.min.js');
  var web3 = new Web3("http://127.0.0.1:7545");
  // window.ethereum.enable();

  // web3.eth.getBalance(account_addr).then((balance) => {

  //   console.log(balance);
      
	// });

  var secrets = [[]];
  var org_paras = [];

  // var para = JSON.stringify(patient_dataset);
  // var secret = 'secret key 123';
  // var encr = CryptoJS.AES.encrypt(para, secret).toString();
  // console.log(encr);
  // var decr = CryptoJS.AES.decrypt(encr, secret).toString(CryptoJS.enc.Utf8);
  // console.log(decr);

  // var encr_priv = CryptoJS.SHA256(encr);

  // The `generateKeyPairSync` method accepts two arguments:
  // 1. The type ok keys we want, which in this case is "rsa"
  // 2. An object with the properties of the key
  const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
    // The standard secure default length for RSA keys is 2048 bits]
    modulusLength: 2048,
    publicKeyEncoding: {
      type: 'spki',       // recommended to be 'spki' by the Node.js docs
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',      // recommended to be 'pkcs8' by the Node.js docs
      format: 'pem',
    }
  });

  // let crypt = new JSEncrypt({default_key_size: '2048'});

  // console.log(publicKey.toString());
  // console.log(privateKey.toString('base64'));

  // console.log(CryptoJS.lib.WordArray.random(128/8).toString());

  var contract = new web3.eth.Contract(abi, smart_contract_addr);

  for (let index = 0; index < patient_dataset.length; index++) {
    var patient = patient_dataset[index];
    var paras = [];
    var encr_sec = [];
    if(index>0)
      secrets.push([]);
    for (let j = 0; j < patient.length; j++) {
      var para = patient[j];
      // console.log(secrets[index].length)
      secrets[index].push(CryptoJS.lib.WordArray.random(128/8).toString());
      para = CryptoJS.AES.encrypt(JSON.stringify(para), secrets[index][secrets[index].length-1]).toString();
      paras.push(para);
    }
    for(let k = patient.length; k<11; k++)
      paras.push("");
    
    const myData = contract.methods.write_all_records([1,2,3,4,5,6,7,8,9,10], "PID"+String(index+1), paras).encodeABI();

    web3.eth.defaultAccount = account_addr;
  
    web3.eth.getTransactionCount(account_addr, (err, txCount) => {
        if(err)
          console.log(err);
        // Build the transaction
        if(nonce_value == txCount)
          nonce_value = nonce_value + 1;
        else
          nonce_value = txCount;
        console.log('Nonce: ' + nonce_value);
        const txObject = {
          nonce:    web3.utils.toHex(nonce_value),
          to:       smart_contract_addr,
          value:    web3.utils.toHex(web3.utils.toWei('0', 'ether')),
          gasLimit: web3.utils.toHex(2000000),
          gasPrice: web3.utils.toHex(web3.utils.toWei('150', 'gwei')),
          data: myData
        }
        // Sign the transaction
        const tx = new Tx(txObject);
        tx.sign(account_private);
    
        const serializedTx = tx.serialize();
        const raw = '0x' + serializedTx.toString('hex');
    
        // Broadcast the transaction
        setTimeout(() => {
          const transaction = web3.eth.sendSignedTransaction(raw, (err, tx) => {
            console.log(tx)
            if(err){
              console.log(err);
              if(index == (patient_dataset.length-1))
                res.json({data: {message: 'Error', error: err.toString()}})
            } 
            else if(index == (patient_dataset.length-1)){
              // console.log(req.body.key);
              // console.log(paras);
              secrets[0].forEach(element => {
                // encr_sec.push(encryptText(element, req.body.key));
                // crypt.setPublicKey(req.body.key);
                // encr_sec.push(crypt.encrypt(element));
                // console.log(element);
                org_paras.push(element);
                key.importKey(req.body.key);
                let e = key.encrypt(element, 'base64');
                encr_sec.push(e);
              });
              // console.log(encr_sec.toString('base64'));
              // res.send("Complete");
              res.json({data: {message: 'Completed', encrypted_secrets: encr_sec, pid: 'PID1'}})
            }
          });
        }, 1500);

      });
  }

  // var encr = CryptoJS.AES.encrypt(org_paras[0], secrets[0][0]);
  // console.log(encr);
  // var decr = CryptoJS.AES.decrypt(encr, secrets[0][0]).toString(CryptoJS.enc.Utf8);
  // console.log(decr);

  // console.log(JSON.stringify(secrets[0]));

  // var encr_sec = encryptText(JSON.stringify(secrets[0]), publicKey.toString());
  // console.log(encr_sec.toString('base64'));

  // var decr_sec = decryptText(encr_sec, privateKey.toString());
  // console.log(decr_sec.toString());

  // var contract = new web3.eth.Contract(abi, smart_contract_addr);

  // const myData = contract.methods.write_record(0, "PID1", encr).encodeABI();

  // web3.eth.defaultAccount = account_addr;

  // web3.eth.getTransactionCount(account_addr, (err, txCount) => {
  //   // Build the transaction
  //     console.log(err);
  //     const txObject = {
  //       from:     account_addr,
  //       nonce:    web3.utils.toHex(txCount),
  //       to:       smart_contract_addr,
  //       value:    web3.utils.toHex(web3.utils.toWei('0', 'ether')),
  //       gasLimit: web3.utils.toHex(2100000),
  //       gasPrice: web3.utils.toHex(web3.utils.toWei('6', 'gwei')),
  //       data: myData
  //     }
  //     // Sign the transaction
  //     const tx = new Tx(txObject, { chain: 'ropsten' });
  //     tx.sign(account_private);
  
  //     const serializedTx = tx.serialize();
  //     const raw = '0x' + serializedTx.toString('hex');
  
  //     // Broadcast the transaction
  //     const transaction = web3.eth.sendSignedTransaction(raw, (err, tx) => {
  //         console.log(tx)
  //         console.log(err)
  //     });
  //   });

  // res.send('Hello World!');
})

// app.post('/api/patient/list_doctors', (req, res) => {
  
//   var web3 = new Web3("http://127.0.0.1:7545");
//   var contract = new web3.eth.Contract(abi, smart_contract_addr);
//   contract.methods.list_all_patients().call({from: account_addr}).then((result) => {
//     console.log(result);
//   });

// });

function encryptText (plainText, key) {
  return crypto.publicEncrypt({
    // key: fs.readFileSync('public_key.pem', 'utf8'),
    key: key,
    padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
    oaepHash: 'sha256'
  },
  // We convert the data string to a buffer
  Buffer.from(plainText)
  )
}

function decryptText (encryptedText, key) {
  return crypto.privateDecrypt(
    {
      // key: fs.readFileSync('private_key.pem', 'utf8'),
      key: key,
      // In order to decrypt the data, we need to specify the
      // same hashing function and padding scheme that we used to
      // encrypt the data in the previous step
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256'
    },
    encryptedText
  )
}

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})