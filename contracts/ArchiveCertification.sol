pragma solidity ^0.5.7;

contract ArchiveCertification{

  struct Certificate{
    uint id;
    address process_owner;
    string name;
    string description;
    string process_data;
    uint256 unique_identifier;
  }

  // state variables
  address payable contract_owner;
  uint certificateCounter;
  mapping (uint => Certificate) public certificates;

  // modifiers
  modifier contractOwner() {
    require(msg.sender == contract_owner);
    _;
  }

  // constructor
  constructor () public {
    contract_owner = msg.sender;
  }

  function getLastBlockTimestamp() public view returns (uint) {
    return  block.timestamp;
  }


  function getContractOwner() public view returns (address){
    return contract_owner;
  }


  // deactivate the contract
  function kill() public contractOwner {
    selfdestruct(contract_owner);
  }

  // events
  event LogSignCertificate(
    uint indexed _id,
    address indexed _process_owner,
    string _name,
    string _process_data
  );

  // events
  event LogModifyCertificate(
    address indexed _process_owner,
    string _name,
    string _process_data
  );

  // events
  event LogModifyProcessOwner(
    address indexed _process_owner,
    string _name
  );


  function signCertificate(address _process_owner, string memory _name, string memory _description, string memory _process_data, uint256 _unique_identifier) public contractOwner{
    // index new certificate
    certificateCounter++;
    // store the certificate
    certificates[certificateCounter] = Certificate(
      certificateCounter,
      _process_owner,
      _name,
      _description,
      _process_data,
      _unique_identifier
     );

    emit LogSignCertificate(certificateCounter, _process_owner, _name, _process_data);
  }

  // fetch the number of certificate in the contract
  function getNumberOfCertificates() public view returns (uint) {
    return certificateCounter;
  }

  function getCertificate(uint _index, uint _unique_identifier) public view returns (string memory, string memory, address, address){
    //require(msg.sender == certificates[_index].process_owner);
    require(certificates[_index].unique_identifier == _unique_identifier);
    return (certificates[_index].name, certificates[_index].process_data, msg.sender, certificates[_index].process_owner);
  }

  function modifyCertificate(uint _index, string memory _information) public {
    require(msg.sender == certificates[_index].process_owner);
    Certificate storage certificate = certificates[_index];
    string memory a = string(abi.encodePacked(certificate.process_data,'§', _information));
    certificate.process_data = a;
    string memory name = certificate.name;
    address process_owner = certificate.process_owner;
    emit LogModifyCertificate(process_owner, name, _information);
  }

  function modifyProcessOwner(uint _index, address _nextProcessOwner, string memory _strNextProcessOwner) public {
    require(msg.sender == certificates[_index].process_owner);
    Certificate storage certificate = certificates[_index];
    certificate.process_owner = _nextProcessOwner;
    string memory name = certificate.name;
    address process_owner = certificate.process_owner;
    string memory a = string(abi.encodePacked(certificate.process_data,'§§', _strNextProcessOwner));
    certificate.process_data = a;
    emit LogModifyProcessOwner(process_owner, name);
  }
  
  function getCertificateOwner(uint _index) public view returns (address){
    Certificate storage certificate = certificates[_index];
    return certificate.process_owner;
  }


}
