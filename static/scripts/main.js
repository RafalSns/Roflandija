$(function(){
    $("#selecter").selectize();
});
document.addEventListener("DOMContentLoaded", function () 
{
    document.querySelectorAll(".movie").forEach(function (movieDiv) {
        movieDiv.onclick = function () {
            
            var movieTitle = this.innerText;
            var moviePoster = this.innerHTML;
            var selectedGenres = this.getAttribute("data-genres");
            var selectedAvarage = this.getAttribute("data-avarage");
            var selectedLang = this.getAttribute("data-lang");
            var selectedOverwiev = this.getAttribute("data-overwiev");
            var selectedDate = this.getAttribute("data-date");
            var selectedVotes = this.getAttribute("data-votes");
            var selectedTrailers = this.getAttribute("data-trailer");

           



            console.log("Selected Genres:" + selectedTrailers );
            var genres = selectedGenres.split(",").map(genre => genre.trim());
            var genreCotainer = document.getElementById("genre-container");

            genres.forEach(genre => {
                button = document.createElement("button");
                button.className = "genre-button";
                button.textContent = genre;
                genreCotainer.appendChild(button);
            });

            const videoId = selectedTrailers.split("v=")[1];
            const embedUrl = `https://www.youtube.com/embed/${videoId}`;

            document.getElementById("traile-container").innerHTML = `
            <iframe 
                width="560" 
                height="315" 
                src="${embedUrl}" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
            </iframe>
            `;
         
            
           
        
            document.getElementById("my_modal").classList.add("open");
            document.getElementById("modal-movie-title").innerText = movieTitle;
            document.getElementById("modal-movie-data").innerText = "(" + selectedDate.substring(0,4) +")";
            document.getElementById("modal-movie-poster").innerHTML = moviePoster;
            document.getElementById("raiting").innerText = selectedAvarage;
            document.getElementById("votes").innerText = selectedVotes;
            document.getElementById("movie-lang").innerText = "Original language: " + selectedLang.toUpperCase();
            document.getElementById("modal-movie-overwiev").innerText = selectedOverwiev;

            
            document.getElementById("close-my-modal-btn").addEventListener("click", function () 
            {
                genreCotainer.innerHTML = "";
                document.getElementById("my_modal").classList.remove("open");
            });

            
        }
    });
});



    


