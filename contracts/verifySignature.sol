pragma solidity ^0.6.1;

contract verifySignature{
    
    address owner;
    
    constructor() public {
        owner = msg.sender;    
    }
    
    function ecrecovery(bytes32 hash, bytes memory sig) internal pure returns (address) {
        bytes32 r;
        bytes32 s;
        uint8 v;
        
        if (sig.length != 65) {
            return address(0);
        }
        
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := and(mload(add(sig, 65)), 255)
        }
        
        if (v < 27) {
            v += 27;
        }
        
        if (v != 27 && v != 28) {
            return address(0);
        }
        
        if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) {
            return address(0);
        }
        
        return ecrecover(hash, v, r, s);
    }
    
    function ecverify(bytes32 hash, bytes memory sig) public view returns (bool) {
        return owner == ecrecovery(hash, sig);
    }
    
}
