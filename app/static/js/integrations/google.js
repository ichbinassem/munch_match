import { get } from "../_api.js";

export async function getImageFromGoogleImages(
  query,
  stopLoading = true,
  createLoading = true
) {
  const encodedQuery = encodeURIComponent(query);
   // Send an HTTP GET request to the Google Custom Search API to search for images
  const response = await get(
    `https://customsearch.googleapis.com/customsearch/v1?key=AIzaSyBBUaCVVNYenmnVL6olLHUFT4A1kfpkd-I&cx=03118f9400a2e4171&q=${encodedQuery}&searchType=image`,
    true,
    stopLoading,
    createLoading
  );

  // Extract the first image URL from the response data that matches the criteria
  const chosenImage = response.data.items
    .map((item) => item.link)
    .filter(
      (link) =>
        link.substring(link.length - 3, link.length) === "png" ||
        link.substring(link.length - 3, link.length) === "jpg" ||
        link.substring(link.length - 4, link.length) === "jpeg"
    )[0];
    
  return chosenImage;
}
