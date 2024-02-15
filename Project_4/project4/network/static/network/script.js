document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('.showallPosts').addEventListener('click',showallPosts);
    showallPosts();
  });


  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function savePost(id){
    changed_data = document.getElementById(`message-text-${id}`).value;
    edit_post = document.getElementById(`content_of_post_${id}`);
    edit_post.innerHTML = "Has wrote: ";
    edit_post.innerHTML += changed_data;
    //Change the read status to read
    fetch(`/edit/${id}`, {
      method: 'PUT',
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json",
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        changed_data : changed_data
      })
    })
  }

  function showallPosts(){
    // Show the mailbox and hide other views
    document.querySelector('#allPosts-view').style.display = 'block';

    // Clear out composition field
    document.querySelector('#allPosts-view').value = '';
    // Show the mailbox name
    document.querySelector('#allPosts-view').innerHTML = `
        <h3 class="text-center">All Posts</h3>
    `;
    // Get data
    const searchParams = new URLSearchParams(window.location.search);
    fetch(`/allPosts?` + new URLSearchParams({
        page: searchParams.get('page') || 1
    }))
    .then(response => response.json())
    .then(result => {
      //Process to get data
      let currentUser_Id = result.currentUser_Id
      for(let i = 0; i < result.posts.length; i++) {
        const newDiv = document.createElement('div');
        newDiv.classList.add('list-group-item');
        let post = result.posts[i];
        let post_timestamp = post.timestamp;
        let post_author = post.author;
        let post_author_id = post.author_id;
        let post_content = post.content;
        let post_likes = post.likes;
        let post_id = post.id;
        let post_likers = post.likers;
        // Add information of that post
        newDiv.innerHTML = `
          <h5>Author: <a href="/profile/${post_author_id}"> ${post_author}</a></h5>
          <h6>At: ${post_timestamp}</h6>
          <p id="content_of_post_${post_id}">Has wrote: ${post_content}</p>
        `;
        // Add the like and unlike button
        if (post_likers.includes(currentUser_Id)) {
          liked_status = true;
          newDiv.innerHTML += `
            <p id="like_no_of_post_${post_id}" class="likes"><a id="like_manager_${post_id}" href="javascript:void(0)" onclick="likeUpdater(${post_id},${currentUser_Id},${liked_status},${post_likes})">Unlike</a>: ${post_likes}</p>  
        `;
        }
        else {
          liked_status = false;
          newDiv.innerHTML += `
            <p id="like_no_of_post_${post_id}" class="likes"><a id="like_manager_${post_id}" href="javascript:void(0)" onclick="likeUpdater(${post_id},${currentUser_Id},${liked_status},${post_likes})">Like</a>: ${post_likes}</p>  
        `;
        }
          
        // Add an edit button
        if (currentUser_Id == post_author_id){
          newDiv.innerHTML += `
            <button type="button" class="btn btn-primary edit_button" data-toggle="modal" data-target="#editPost_${post_id}">Edit</button>
          `;
        }

        // Add a modal
        newDiv.innerHTML += `
            <div class="modal" tabindex="-1" role="dialog" id=editPost_${post_id} aria-labelledby="editPost_${post_id}_Label" aria-hidden="true">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Editting your post</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                      <div class="form-group">
                        <label for="message-text-${post_id}" class="col-form-label">Content:</label>
                        <textarea class="form-control" id="message-text-${post_id}">${post_content}</textarea>
                      </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-primary" onclick="savePost(${post_id})" data-dismiss="modal">Save changes</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
          </div>
        `;
        document.querySelector('#allPosts-view').append(newDiv);
      }
      
      // Add pagination
      page = result.page;
      var navElement = document.createElement("nav");
      var ulElement = document.createElement("ul");
      ulElement.classList.add('pagination');
      if (page.has_previous) {
        ulElement.innerHTML += `
          <li class="page-item"><a class="page-link" href="?page=1">&laquo; first</a></li>
          <li class="page-item"><a class="page-link" href="?page=${page.previous_page}">previous</a></li>
        `;
      }
      ulElement.innerHTML += `
        <li class="page-item mx-3">
          <p class="text-center mt-2"> Page ${page.current_page} of ${page.num_pages} </p>
        </li>
      `;
      if (page.has_next) {
        ulElement.innerHTML += `
          <li class="page-item"><a class="page-link" href="?page=${page.next_page}">next</a></li>
          <li class="page-item"><a class="page-link" href="?page=${page.num_pages}">last &raquo;</a></li>
        `;
      }
      navElement.appendChild(ulElement);
      document.querySelector('#toggle').append(navElement);
    })
  }

  function likeUpdater(post_id,currentUser_Id, liked_status,post_likes){
    if (liked_status==false) {
      displayLikes = document.getElementById(`like_no_of_post_${post_id}`);
      post_likes +=1
      displayLikes.innerHTML = `  
        <p id="like_no_of_post_${post_id}" class="likes"><a id="like_manager_${post_id}" href="javascript:void(0)" onclick="likeUpdater(${post_id},${currentUser_Id},${!liked_status},${post_likes})">Unlike</a>: ${post_likes}</p>
      `;

      fetch(`/like_update`, {
        method: 'PUT',
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_id : post_id,
          currentUser_Id : currentUser_Id
        })
      })
    }
    else {
      displayLikes = document.getElementById(`like_no_of_post_${post_id}`);
      post_likes -=1
      displayLikes.innerHTML = `  
        <p id="like_no_of_post_${post_id}" class="likes"><a id="like_manager_${post_id}" href="javascript:void(0)" onclick="likeUpdater(${post_id},${currentUser_Id},${!liked_status},${post_likes})">Like</a>: ${post_likes}</p>
      `;
      fetch(`/unlike_update`, {
        method: 'PUT',
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_id : post_id,
          currentUser_Id : currentUser_Id
        })
      })
    }
  }
