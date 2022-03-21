//SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract BollingerBandsRelated {


    function testGetBollingerBands() public pure returns (uint[10] memory){  

        uint[10] memory exampleInput = [uint(1), 2, 3, 4, 5, 6, 7,8,9,0];

        (
            uint[10] memory smaBand,
            uint[10] memory lowerBand,
            uint[10] memory upperBand
        ) =  getBollingerBands(exampleInput, 2);

        // return bollingerBands.smaBand;

        return smaBand;

    } 

    function getSMA(uint[10] memory sequence) public pure returns (uint) {
        uint sum = 0;
        uint i = 0;
        for (i; i < sequence.length; i++) {
            sum = sum + sequence[i];
        }

        return sum / sequence.length;
    }
    

    function getBollingerBands(uint[10] memory sequence, uint spreadFactor) public pure returns (uint[10] memory, uint[10] memory, uint[10] memory){  
            
        uint i = 0;

        uint[10] memory smaBand = [uint(10), 20, 30, 40, 50, 60, 3,4,5,6];
        uint[10] memory lowerBand = [uint(10), 20, 30, 40, 50, 60, 3,4,5,6];
        uint[10] memory upperBand = [uint(10), 20, 30, 40, 50, 60, 3,4,5,6];

        // uint[] memory smaArray;
        for (i; i < sequence.length; i++) {
            smaBand[i] = i;
        }


         return (smaBand, lowerBand, upperBand);  
        
    }   

}


