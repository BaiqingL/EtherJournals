pragma solidity ^0.5.0;

contract Account {
    uint private num;
    address private owner;

    modifier ownerFunc {
        require(owner == msg.sender);
        _;
    }

    constructor(uint delta) public {
        num = delta;
        owner = msg.sender;
    }
    
    // Allow anyone to add data
    function deposit(uint delta) public {
        num += delta;
    }

    // Restrict to owner
    function withdraw(uint delta) public ownerFunc {
        if (num >= delta) {
            num -= delta;
        }
    }

    function viewData() public view returns (uint) {
        return num;
    }

}
