// SPDX-License-Identifier: MIT 

pragma solidity ^0.8.7;

import '@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol';
import '@uniswap/v3-periphery/contracts/libraries/TransferHelper.sol';
import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

contract VoFarmPool{

    //
    string public lastAdvice = ""; 
    string private contractName = "";

	// swapping
    ISwapRouter private swapRouter;
	uint24 private constant poolFee = 500;

	// Rinkeby:
    address public stable; 
    address public volat;
       
    // Debug -- teilweise später wieder auf private
    string[] advices;
    uint256 public lastCallback;

    //------ trading setup
    //Array of prices: volatile coin - stable coin
    uint256[] prices;

    uint256 minStableDeposit;
    uint256 minVolatileDeposit;

    // represents 100% of the stake
    uint256 totalSupply = 1000000000000000000;

    //all invested addresses
    address[] public investors;

    //address -> stake in pool
    mapping(address => uint256) public stakes;

    //contract stable state: stable=true, volatile=false
    bool public stableState = false;
	
	//------ basic address setup
    // basic input for settings: [10,6,5,5,1,1]
    // basic router-address for rinkeby/ropsten-net: 0xE592427A0AEce92De3Edee1F18E0157C05861564
	constructor(
        string memory _name, 
        address _primary, 
        address _secundary, 
        address _router,
        uint256 _minStableDeposit,
        uint256 _minVolatileDeposit)
    {
        // Token Settings
        stable = _primary;
        volat = _secundary;
        contractName = _name;
        minStableDeposit = _minStableDeposit;
        minVolatileDeposit = _minVolatileDeposit;

        swapRouter = ISwapRouter(_router);

    }

//-----------------------------
// Gettes functions / interaction

    function name() public view returns(string memory)
    {
        return contractName;
    }

    function _getPrice(address _token) public view returns(uint256)
    {
        return IERC20(_token).balanceOf(address(this));
    }

    function _getLastAdvice() public view returns(string memory)
    {
        return lastAdvice;
    }

    function _getPriceList() public view returns(uint[] memory)
    {
        return prices;
    }

    function _getAdviceCount() public view returns(uint256)
    {
        return advices.length;
    }

    function _getAdviceAtCount(uint256 _id) public view returns(string memory)
    {
        return advices[_id-1];
    }

    function getPrimaryToken() public view returns(address)
    {
        return stable;
    }

    function getSecondaryToken() public view returns(address)
    {
        return volat;
    }

    function getCurrentToken() public view returns(address)
    {
        if (stableState){
            return stable;
        } else {
            return volat;
        }
    }

    function setStableState(bool _newValue) public
    {
        stableState = _newValue;
    }


//-----------------------------
// Pool functions

	function swapExcactInToOut(
        uint256 amountIn, 
        address tokenIN, 
        address tokenOUT
        ) 
        public 
        returns (bool) {
    
        // Approve the router to spend DAI.
        TransferHelper.safeApprove(tokenIN, address(swapRouter), amountIn);

        // Naively set amountOutMinimum to 0. In production, use an oracle or other data source to choose a safer value for amountOutMinimum.
        // We also set the sqrtPriceLimitx96 to be 0 to ensure we swap our exact input amount.
        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: tokenIN,
                tokenOut: tokenOUT,
                fee: poolFee,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap. Retrun true if the swap was succesfull
        if (swapRouter.exactInputSingle(params) > 0) 
        {
            return true;
        }
        else
        {
            return false;
        }
    }

//-----------------------------
// Pool - Stake-Handling

//Funktionen werden noch korrekt implementiert
    //CRUD functions for mapping
    function getInvestorStake(address _address) public view returns (uint256)
    {
        return stakes[_address];
    }

    function removeInvestorAddress(address _address) public
    {
        //remove stake
        delete stakes[_address];
        //remove address from stored addresses
        uint256 investorsLength = investors.length;
        require(investorsLength > 0, "Cannot remove elements from empty array");
        address[] memory investorsTemp = new address[](investorsLength-1);
        
        uint c=0;
        for(uint i=0; i<investorsLength; i++){
            if(investors[i]!=_address){
                investorsTemp[c] = investors[i];
                c++;
            }
        }
        
        delete investors;
        
        for(uint i=0; i<investorsLength-1; i++){
            investors.push( investorsTemp[i] );
        }
    }
    
    function addInvestorAddress(address _address) private {
        require(_investorsContainsAddress(_address) == false, "Address already stored.");
        investors.push(_address);
    }
    
    function _investorsContainsAddress(address _address) 
    private 
    view 
    returns (bool){
        for(uint i=0;i<investors.length;i++){
            if(investors[i] == _address){
                return true;
            }
        }
        return false;
    }
    
    function _sumInvestorStakes() 
    private 
    view
    returns (uint256){
        uint256 sum = 0;
        for(uint i=0; i<investors.length; i++){
            sum = sum + stakes[investors[i]];
        }
        return sum;
    }

    function _smallestInvestorByStake() 
    private 
    view 
    returns (address){
        address investor = investors[0];
        for(uint i=1; i<investors.length; i++){
            if(stakes[investors[i]] < stakes[investor]){
                investor = investors[i];
            }
        }
        return investor;
    }
    
    function recalculateAllStakesOnDeposit(uint256 amount) private {
        uint256 oldBalance = this.balance() - amount;
        for(uint i=0; i<investors.length; i++){
            stakes[investors[i]] = (stakes[investors[i]]*oldBalance)/(oldBalance + amount);
        }
    }

    function recalculateAllStakesOnWithdraw(uint256 amount) private {
        if(investors.length == 1){
            //stake = total supply
            stakes[investors[0]] = totalSupply;
        }else{
            if(investors.length > 0){
                //calculate stakes
                uint256 oldBalance = this.balance();
                for(uint i=0; i<investors.length; i++){
                    stakes[investors[i]] = (stakes[investors[i]]*oldBalance)/(oldBalance - amount);
                }
                //divide remainder between investors
                uint256 remainder = totalSupply - _sumInvestorStakes();
                uint256 share = remainder / investors.length;
                if(share > 0){
                    for(uint i=0; i<investors.length; i++){
                        stakes[investors[i]] = stakes[investors[i]] + share;
                    }
                }
                address smallest = _smallestInvestorByStake();
                stakes[smallest] = stakes[smallest] + (remainder - share * investors.length);
            }
        }
    }
    
    function balance() public view returns (uint256){
        //hier aus beiden token wert errechnen, der eth wei einheit entspricht
        //tokenpreise müssen mit oracle abgefragt werden-> nicht unbedingt

        if(stableState){
            return ERC20(stable).balanceOf(address(this));
        }else{
            return ERC20(volat).balanceOf(address(this));
        }
    }
 
    function deposit(address _token, uint _amount) public{
        //can only deposit token depending on contract state, check validity and approve/reject
        //check for minimum deposit values
        if(stableState){
            require(_token==address(ERC20(stable)),"Please use stable token to deposit.");
            require(_amount>=minStableDeposit,"require minimum amount of stable-token");
        }else{
            require(_token==address(ERC20(volat)),"Please use volatile token to deposit.");
            require(_amount>=minVolatileDeposit,"require minimum mount of volatile-token");
        }

        //add tokens to pool
        ERC20(_token).transferFrom(msg.sender, address(this), _amount);

        //assign new stakes for everyone, add address to investors on first deposit
        if(investors.length < 1){
            addInvestorAddress(msg.sender);
            stakes[msg.sender] = totalSupply;
        }else{
            if(!_investorsContainsAddress(msg.sender)){
                addInvestorAddress(msg.sender);
            }
            recalculateAllStakesOnDeposit(_amount);
            stakes[msg.sender] = totalSupply - _sumInvestorStakes() + stakes[msg.sender];
        }
    }
    
    function withdraw() 
    external 
    payable
    {
        require(_investorsContainsAddress(msg.sender), "Address not investor.");
        uint256 amount = (stakes[msg.sender]*this.balance())/totalSupply;
        removeInvestorAddress(msg.sender);
        recalculateAllStakesOnWithdraw(amount);
        //(bool success, ) = //msg.sender.call{value:amount}("");
        if(stableState){
            ERC20(stable).transfer(msg.sender, amount);
        }else{
            ERC20(volat).transfer(msg.sender, amount);
        }
        //require(success, "Transfer failed.");
    }

    function getEarned(address _address) public view returns (uint256)
    {
        return (getInvestorStake(_address) * balance()) / totalSupply;
    }
}
