contract HelloWorld{
    uint balance;
    
    //constructor name has to be same as contract
    //runs once upon contract creation
    //runs on deploy and never again
    function HelloWorld(){
    //Computation costs gas, while storing values to the blockchain would be more expensive compared to addition and subtraction
        balance = 69;
        
    }
    //Solidity real time complier
    //Contract address on testnet 0xbbf289d846208c16edc8474705c748aff07732db
}
