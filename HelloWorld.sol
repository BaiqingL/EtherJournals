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
}
