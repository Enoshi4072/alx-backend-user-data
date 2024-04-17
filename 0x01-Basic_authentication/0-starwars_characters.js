#!/usr/bin/node

// Importing necessary modules
const request = require('request');

// Function to fetch and print characters of a Star Wars movie
function fetchCharacters(movieId) {
    // URL of the Star Wars API endpoint to fetch movie information
    const url = `https://swapi-api.alx-tools.com/api/films/${movieId}/`;

    // Making HTTP GET request to fetch movie information
    request(url, (error, response, body) => {
        if (error) {
            console.error('Error fetching movie information:', error);
            return;
        }

        if (response.statusCode !== 200) {
            console.error('Failed to fetch movie information. Status code:', response.statusCode);
            return;
        }

        // Parsing JSON response
        const movieInfo = JSON.parse(body);

        // Fetching and printing character names
        const characterUrls = movieInfo.characters;
        fetchCharactersInfo(characterUrls);
    });
}

// Function to fetch and print character names
function fetchCharactersInfo(characterUrls) {
    characterUrls.forEach(characterUrl => {
        // Making HTTP GET request to fetch character information
        request(characterUrl, (error, response, body) => {
            if (error) {
                console.error('Error fetching character information:', error);
                return;
            }

            if (response.statusCode !== 200) {
                console.error('Failed to fetch character information. Status code:', response.statusCode);
                return;
            }

            // Parsing JSON response
            const characterInfo = JSON.parse(body);
            console.log(characterInfo.name);
        });
    });
}

// Getting movie ID from command-line arguments
const movieId = process.argv[2];

// Validating movie ID
if (!movieId || isNaN(movieId)) {
    console.error('Please provide a valid movie ID.');
    process.exit(1);
}

// Fetching and printing characters of the specified movie
fetchCharacters(movieId);
