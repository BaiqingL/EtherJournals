pragma solidity ^0.6.1;

// Verifies the signature using the message and the signature

contract verifySignature{

    address owner;

    constructor() public {
        owner = msg.sender;    
    }

    function ecrecovery(
        bytes32 hash,
        bytes memory sig
    ) 
        internal
        pure
        returns (address) 
    {
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

    if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) {
        return address(0);
    }

    if (v < 27) {
        v += 27;
    }

    if (v != 27 && v != 28) {
        return address(0);
    }
    
        return ecrecover(hash, v, r, s);
    }
    
    function uintToString(
        uint v
    )
        pure
        internal
        returns (string memory)
    {
        uint w = v;
        bytes32 x;
        if (v == 0) {
            x = "0";
        } else {
            while (w > 0) {
                x = bytes32(uint(x) / (2 ** 8));
                x |= bytes32(((w % 10) + 48) * 2 ** (8 * 31));
                w /= 10;
            }
        }

        bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }

        bytes memory resultBytes = new bytes(charCount);
        uint j = 0;
        for (j = 0; j < charCount; j++) {
            resultBytes[j] = bytesString[j];
        }
        return string(resultBytes);
    }

    function hash_msg(
        string memory _msg
    ) 
        internal
        pure
        returns (bytes32)
    {
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n", uintToString(bytes(_msg).length), _msg));
    }

    function ecverify(
        string memory _msg,
        bytes memory sig
    ) 
        public
        view
        returns (bool) 
    {
        return owner == ecrecovery(hash_msg(_msg), sig);
    }

}
