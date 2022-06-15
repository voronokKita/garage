function fun()
{
    // Get form value
    var line = document.getElementById('name').value;

    if (line.length > 0) {
        line = "Hello, " + line + "!";
    }
    else {
        line = "Hello, World!";
    }
    line += "<br>Sorry for being lazy on this page :)";

    // Output
    document.getElementById('result').innerHTML = line;
}
