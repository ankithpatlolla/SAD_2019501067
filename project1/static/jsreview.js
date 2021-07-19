document.addEventListener('DOMContentLoaded', () => {
    console.log("Testing");
    // function renderHTML() {
    document.querySelector('#review').onsubmit = () => {
        var rate = "";
        document.querySelector('#result').innerHTML = ""
        var x = document.getElementsByName("rating")
        for (let i = 0; i < x.length; i++) {
            if (x[i].checked === true) {
                rate = x[i].value
            }
        }
        var isbn = document.getElementById("book_isbn").name;
        console.log(isbn)
        //Initialise new Request
        const request = new XMLHttpRequest();
        // const rate = document.querySelector('rate').value;
        const comment = document.querySelector('#comment').value;
        console.log("before request opening")
        request.open('POST',('/api/submit_review/'+(isbn)+""))
        console.log("after request opened")
        request.onload = () => {
            //extract JSON data from request
            // request.responseType = 'json';
            const data = JSON.parse(request.responseText);
            console.log(data)
            //update the result div
            if (data.reviews["status"] === "200") {
                let contents = '<li>' + 'rating is '+data.reviews["rate"] + '</li>' 
                contents += '<li>' + 'comments are ' + data.reviews["comment"] + '</li>'
                // const contents = ` Your rating --  ${data.reviews["rate"]} your comment -- ${data.reviews["comment"]} `
                document.querySelector('#result').innerHTML = contents;
                
            }
            else if (data.reviews["status"] === "400") {
                let contents = '<li>' + 'rating is'+data.reviews["rate"] + '</li>' 
                contents += '<li>' + 'comments are ' + data.reviews["comments"] + '</li>'
                
                // const contents = ` Your rating --  ${data.reviews["rate"]} your comment -- ${data.reviews["comment"]} `
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
            document.querySelector('#review').innerHTML = ''
        }

        // Add data to send with request
        const data = new FormData();
        data.append('rate', rate)
        data.append('comment', comment);
        // Send request
        request.send(data);
        return false;


    };
});

function secpage() {
    document.querySelector('#review').innerHTML = '<h1>Rating</h1>' +
                '<input name = "rating" value = "1" id = "1"  type="radio" />1 '+ 
                '<input name = "rating" value = "2" id = "2"  type="radio" />2 ' +
                '<input name = "rating" value = "3" id = "3"  type="radio" />3 ' +
                '<input name = "rating" value = "4" id = "4"  type="radio" />4 ' +
                '<input name = "rating" value = "5" id = "5"  type="radio" />5 ' +
                '<div> ' +
                    '<label for="comment">Comment:</label> ' +
                    '<textarea rows="3" id="comment" name="text"></textarea> ' +
                '</div> ' +
                '<button id = "sub" type="submit" name = "action" value = "comment">Submit</button> ' +
            '</form> </div> '
}