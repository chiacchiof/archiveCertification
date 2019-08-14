App = {
  web3Provider: null,
  contracts: {},
  account: 0x0,
  loading: false,
  certificateIDBC : null,
  init: function() {
      showPosition();
    return App.initWeb3();
  },
    
  createQRCodeAccount:function(account){
      //QRCode = require('qrcode');
      canvas = document.getElementById('QRCodeCanvasAccount');
      QRCode.toCanvas(canvas, account.toString(), function(error){
          if(error) console.error(error)
          console.log('qrcode account success!');
      })
  },

  createQRCode:function(account,elementAccountId){
  //QRCode = require('qrcode');
  canvas = document.getElementById(elementAccountId);
  QRCode.toCanvas(canvas, account.toString(), function(error){
      if(error) console.error(error)
      console.log('qrcode account success!');
  })
  },
    
  createQRCodeCertificate:function(infoCertificate){
      //QRCode = require('qrcode');
      canvas = document.getElementById('QRCodeCanvasProd');
      QRCode.toCanvas(canvas, infoCertificate, function(error){
          if(error) console.error(error)
          console.log('qrcode certificate success!');
      })
  },
    
    initWeb3: function() {
    // initialize web3
    if(typeof web3 !== 'undefined') {
      //reuse the provider of the Web3 object injected by Metamask
      App.web3Provider = web3.currentProvider;
    } else {
      //create a new provider and plug it directly into our local node
      App.web3Provider = new Web3.providers.HttpProvider("https://ropsten.infura.io/v3/bd3f6da3dd35401483729f00acfe5496");
      //App.web3Provider = new Web3.providers.HttpProvider("127.0.0.1:7545");    
    }
    web3 = new Web3(App.web3Provider);
    urlParams = new URLSearchParams(window.location.search);
    certificateIDBC = urlParams.get('ID');
    certificateUniqueID = urlParams.get('UniqueIdentifier');
      
    App.displayAccountInfo();
    return App.initContract();
  },
  
  displayAccountInfo: function() {
    web3.eth.getCoinbase(function(err, account) {
      if(err === null) {
        App.account = account;
        //$('#account').text(account);
        web3.eth.getBalance(account, function(err, balance) {
          if(err === null) {
            $('#accountBalance').text(web3.fromWei(balance, "ether") + " ETH");
          }
        })
      }
    });
  },

  initContract: function() {
    $.getJSON('ArchiveCertification.json', function(archiveCertificationArtifact) {
      // get the contract artifact file and use it to instantiate a truffle contract abstraction
      App.contracts.ArchiveCertification = TruffleContract(archiveCertificationArtifact);
      // set the provider for our contracts
      App.contracts.ArchiveCertification.setProvider(App.web3Provider);
      // listen to events
      App.listenToEvents();
      // retrieve the article from the contract
      return App.reloadCertification();
    });
  },
    
   reloadCertification: function(){
         // avoid reentry
        if(App.loading) {
            return;
        }
        App.loading = true;
        $("#certificateProcessInfo").empty();
        // refresh account information because the balance might have changed
        App.displayAccountInfo();

        App.contracts.ArchiveCertification.deployed().then(function(instance) {
          ArchiveCertificationInstance = instance;
          return ArchiveCertificationInstance.getCertificate(certificateIDBC, certificateUniqueID);
        }).then(function(certificationInfo) {
          // retrieve the article placeholder and clear it
         if(certificationInfo[3]===App.account){
             $('#trackForm').show();
         } $('#certificateName').text(certificationInfo[0]);
          
          var processOwners = (certificationInfo[1]).split("§§");
          
          qrcodeCounter = 0;
          for (i=1;i<processOwners.length;i++){
            var processInfo = (processOwners[i]).split("§");
            for (j=1;j<processInfo.length;j++){
                var markup = "<tr><td><canvas id='QRCodeCanvasAccountId_"+(qrcodeCounter)+"' class='QRCode'/></td><td>" + processInfo[j] + "</td><td>32.45422; 16.4523222 </td><td> 18:15:23 11-02-19</td></tr>";
                $("table tbody").append(markup);
                App.createQRCode(processInfo[i-1],'QRCodeCanvasAccountId_'+(qrcodeCounter));
                qrcodeCounter = qrcodeCounter+1;
            }
         }
          App.createQRCodeCertificate(certificationInfo[0]+"&"+certificationInfo[1]); 
          App.createQRCodeAccount(App.account); 
                
          App.loading = false;
        }).catch(function(err) {
          console.error(err.message);
          App.loading = false;
        });
    },
    
    modifyStatus: function() {
    if (confirm("Sure to modify the status?")) {
        // retrieve the detail of the article
        var _newStatus = $('#newstatus').val();
        App.contracts.ArchiveCertification.deployed().then(function(instance) {
          return instance.modifyCertificate(certificateIDBC,_newStatus, {
            from: App.account,
            gas: 500000
          });
        }).then(function(result) {
            $('#newstatus').val("");
        }).catch(function(err) {
          console.error(err);
        });
    }    
  },
    
    modifyProcessOwner: function() {
    if (confirm("Sure to modify the owner?")) {
        // retrieve the detail of the article
        var _newOwner = $('#newowner').val();
        App.contracts.ArchiveCertification.deployed().then(function(instance) {
          return instance.modifyProcessOwner(certificateIDBC,_newOwner, _newOwner, {
            from: App.account,
            gas: 500000
          });
        }).then(function(result) {
            $('#newowner').val("");
        }).catch(function(err) {
          console.error(err);
        });
    }    
  },
    
    //LogModifyCertificate, LogModifyProcessOwner
      // listen to events triggered by the contract
  listenToEvents: function() {
    App.contracts.ArchiveCertification.deployed().then(function(instance) {
      instance.LogModifyCertificate({}, {}).watch(function(error, event) {
        if (!error) {
         // $("#certificateProcessInfo").append('<li class="list-group-item">' + event.args._process_data + '</li>');
        } else {
          console.error(error);
        }
        $("#TrackOperationTable tbody").empty(); 
        App.reloadCertification();
      });

      instance.LogModifyProcessOwner({}, {}).watch(function(error, event) {
        
        App.reloadCertification();
      });
    });
  },
};

$(function() {
     $(window).load(function() {
          App.init();
     });
});
