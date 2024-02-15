document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //Add event handler
  document.querySelector('#compose-form').addEventListener('submit', process_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function change_archive(email,id){
  console.log("I am here");
  console.log(id);
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })
  .then(response =>response.text())
  .then( result => {
      load_mailbox('inbox')
    })
  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  console.log(mailbox);
  // Get emails from a category
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);

    //Process to get data
    for(let i = 0; i < result.length; i++) {
      const newDiv = document.createElement('div');
      newDiv.classList.add('list-group-item');
      let email = result[i];
      //Change background color based on read status
      if (email.read) {
        newDiv.classList.add("bg-light");
      }
      let email_subject = email.subject;
      let email_timestamp = email.timestamp;
      let email_sender = email.sender;
      newDiv.innerHTML = `
        <h5>Subject: ${email_subject}</h5>
        <h6>Sender: ${email_sender}</h6>
        <p>Timestamp: ${email_timestamp}</p>
      `;
      newDiv.addEventListener('click', function(){
        viewEmail(email.id)
      });
      document.querySelector('#emails-view').append(newDiv);
    }
  });   
}

function reply_email(email){
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  // Fill in composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  let subject = email.subject;
  if (subject.split(' ',1)[0]!="Re:"){
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  else {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  }
  document.querySelector('#compose-body').value = `\r\n On ${email.timestamp}, ${email.sender} wrote: \r\n" ${email.body} " `;
  document.querySelector('#compose-body').value += `\r\n--------------------------------`;
  document.querySelector('#compose-body').value += `\r\n--------------------------------\r\n\r\n`;
}

function viewEmail(id){  
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Show the mail and hide other views
      document.querySelector('#email-view').style.display = 'block';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      // Display the the email
      document.querySelector('#email-view').innerHTML = `
      <p><strong>Subject: </strong>${email.subject}</p>
      <p><strong>From: </strong>${email.sender}</p>
      <p><strong>To: </strong>${email.recipients}</p>
      <p><strong>At: </strong>${email.timestamp}</p>
      <p><strong>Content: </strong></p>
      <p>${email.body}</p>
      `;

      // Button to archive email
      if (email.archived) {
        document.querySelector('#email-view').innerHTML+= `
          <button type="button" class="btn btn-primary" id="archive-control">Unarchive</button>
        `;
      }
      else {
        document.querySelector('#email-view').innerHTML+= `
          <button type="button" class="btn btn-primary" id="archive-control">Archive</button>
        `;
      }
      //Button to reply email
      document.querySelector('#email-view').innerHTML+= `
          <button type="button" class="btn btn-primary" id="reply">Reply</button>
      `;
      document.querySelector('#reply').addEventListener('click', function(){
        reply_email(email);
      });
      document.querySelector('#archive-control').addEventListener('click', function(){
        change_archive(email,email.id);
      });
  });


  //Change the read status to read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

}

function process_email(event){
  event.preventDefault();

  // Get data from the form
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  // Transmit the data to the web
  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
   })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
}