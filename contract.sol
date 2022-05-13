pragma solidity ^0.4.25;

contract Key {
    string public p_key;
    address admin;
    modifier onlyAdmin(){
        require(msg.sender == admin);
        _;
    }
    constructor() public{
        admin = msg.sender;
        p_key = '-';
    }
    function init_key() public {
        p_key = '-';
    }
    
    function set_key(string memory _key) public onlyAdmin{
        p_key = _key;
    }
    
    function disp_key() view public returns (string memory) {
        return p_key;
    }
}
