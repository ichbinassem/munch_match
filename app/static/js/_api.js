import { createLoading, removeLoading } from "./_helper.js";

// Function to make a POST request with the given url, body, and options
export async function post(
  url,
  body,
  fullPath = false,
  stopLoading = true,
  loading = true
) {
  try {
    if (loading) createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(newUrl, {
      // Make the POST request with the given body and headers
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    // Get the data and status from the query response
    const data = await query.json();
    const status = query.status;

    if (stopLoading) removeLoading();
    return { status, data };
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

// Function to make a GET request with the given url and options
export async function get(
  url,
  fullPath = false,
  stopLoading = true,
  loading = true
) {
  try {
    if (loading) createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(newUrl, {
      // Make the GET request with the given headers
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await query.json();
    const status = query.status;

    if (stopLoading) removeLoading();
    return { status, data };
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

// Function to make a PATCH request with the given url, body, and options
export async function patch(
  url,
  body,
  fullPath = false,
  stopLoading = true,
  loading = true
) {
  try {
    if (loading) createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    // Make the PATCH request with the given body and headers
    const query = await fetch(newUrl, {
      method: "PATCH",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    if (stopLoading) removeLoading();
    return status;
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

// Sends a DELETE request to the specified URL with the provided item
export async function remove(
  url,
  item,
  fullPath = false,
  stopLoading = true,
  loading = true
) {
  try {
    if (loading) createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    // Send the DELETE request with the item ID in the URL and a JSON content type header.
    const query = await fetch(`${newUrl}/${item}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    if (stopLoading) removeLoading();
    return status;
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}
