class BoggleGame {

    constructor(boardId, secs = 60) {
        this.boardId = boardId;
        this.secs = secs;
        this.board = $('#' + boardId);
        this.score = 0;
        this.duplicates = []

        //calls initially to display time amount, the updates timer and markup
        this.createMarkup();
        this.timer = setInterval(this.showTimer.bind(this), 1000);

        // listens for form submit //
        $(".guess", this.board).on("submit", this.handleSubmit.bind(this));
        
        
    }

    //Runs all functions required for startup//
    async createMarkup(){
        const response = await axios.get('/data')
        this.showTimer()
        this.showScore()
        this.showHighscore(response.data)
    }

    // Create markup and increment timer, stop interval if time is up // 
    showTimer(){
        $("#timer").text(`Time Left: ${this.secs}`);
        if (this.secs == 0) {
            clearInterval(this.timer);
            this.gameOver();
        }
        this.secs -= 1;
    }

    //adds text and properties to element//
    showMessage(msg, cls){
        $('#container').text(msg).removeClass().addClass(cls);
    }

    //Adds text to highscore div, prevents showing of undefined on first play//
    showHighscore(res){
        if (!res.highscore > 0 ){
            $('#highscore').text(`Highscore: 0`)
        }else{
            $('#highscore').text(`Highscore: ${res.highscore}`)
        }
        
    }

    //adds score to markup//
    showScore(){
        $('.scores').text(`Current Score: ${this.score}`);
    }

    async handleSubmit(evt) {
        evt.preventDefault();

        // If timer is at 0, dont handle data //
        if(this.secs < 0){ 
            return; 
        }else{
        // grabbing data from input //
            const $guess = $('.word', this.board);
            const value = $guess.val()
            const word = value.toUpperCase();

            if (this.checkDuplicate(word) == false){
                $guess.val('');
                return;
            }
            
            // get request and response data // 
            const response = await axios.get('/check-word', { params: { word: word}});
            const isWord = response.data.result;
            
            // checks for markup on page //
            if(!$('#container').text){
                $('#container').empty();
            }

            // custom messages based on word guess //
            if(isWord == 'ok'){  
                this.score += word.length;
                this.showMessage('Good Find!', isWord);
                this.showScore();
                
            }else if(isWord == 'not-on-board'){
                this.showMessage('That word is not on the board', isWord);

            }else{
                this.showMessage('That is not a word', isWord);
            }

            //clear input field//
            $guess.val('');
        }
    }

    // Sends score to server to change session storage
    async gameOver(){
        const response = await axios.post('/game-stats', { score: this.score})       
    }

    checkDuplicate(word){
        for(let val in this.duplicates){
            if (word == this.duplicates[val]){
                this.showMessage('You have already guessed this word!', 'duplicate')
                return false;
            }
        }
        this.duplicates.push(word)
        return true;
            
    }
}