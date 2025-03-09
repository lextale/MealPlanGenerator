      $(document).ready(function() {
          $('#chatForm').submit(function(event) {
              event.preventDefault();
              sendMessage();
          });

          $('#messageInput').on('keypress', function(event) {
              if (event.which === 13 && !event.shiftKey) {  // Check if Enter is pressed and not Shift
                  event.preventDefault(); // Prevent the newline character
                  sendMessage();
              }
          });

          function sendMessage() {
              let userMessage = $('#messageInput').val().trim();
              if (!userMessage) return;

              // Disable the send button and show spinner
              $('#sendButton').prop('disabled', true);
              $('#sendButton').addClass('disabled');
              $('button-spinner').removeClass('hidden');
              $('.button-text').addClass('hidden');
              document.getElementById('messageInput').disabled = true;
              document.getElementById('messageInput').placeholder = "Generating answer...";

              // Convert newlines into <br> elements for proper display of multi-line messages
              let formattedUserMessage = userMessage.replace(/\n/g, '<br>');

              // Append user's message to the chat
              $('#chatMessages').append(`
                  <div class="message sent">
                      <div class="message-content">${formattedUserMessage}</div>
                  </div>
              `);

              // Scroll to the bottom when a new message is added
              $('#chatMessages').scrollTop($('#chatMessages')[0].scrollHeight);

              // Clear the input field
              $('#messageInput').val('');

              // Send message to backend via AJAX
              console.log('Sent post request:', new Date().toLocaleString())
              $.ajax({
                  url: '/chat',
                  method: 'POST',
                  contentType: 'application/json',
                  data: JSON.stringify({ message: userMessage }),
                  success: function(data) {
                      if (data.error) {
                          $('#chatMessages').append(`
                              <div class="message received error">
                                  <div class="message-content">Error: ${data.error}</div>
                              </div>
                          `);
                      } else {
                          // Convert newlines into <br> elements for proper display of multi-line messages in the response
                          let formattedResponseMessage = data.response.replace(/\n/g, '<br>');

                          $('#chatMessages').append(`
                              <div class="message received">
                                  <div class="message-content">${formattedResponseMessage}</div>
                              </div>
                          `);
                      }
                  },
                  error: function() {
                      $('#chatMessages').append(`
                          <div class="message error">
                              <div class="message-content">Something went wrong. Please try again.</div>
                          </div>
                      `);
                  },
                  complete: function() {
                      // Re-enable the button and hide spinner
                      $('#sendButton').prop('disabled', false);
                      $('button-spinner').addClass('hidden');
                      $('.button-text').removeClass('hidden');
                      $('#sendButton').removeClass('disabled');
                      document.getElementById('messageInput').disabled = false;
                      document.getElementById('messageInput').placeholder = "Type a message...";

                      $('#chatMessages').scrollTop($('#chatMessages')[0].scrollHeight);
                    console.log('Completed post request:', new Date().toLocaleString())
                  }
              });
          }

          // Auto-resize the textarea based on input
          $('#messageInput').on('input', function() {
              this.style.height = 'auto'; // Reset the height
              this.style.height = this.scrollHeight + 'px'; // Set the height to match scrollHeight
          });
      });