//Call login modal on page's load if no session is active
$(window).ready(function()
{
	$.getJSON('/_isLogged', {}, function(data)
	    {
	    	if (data.nsfw == 0) 
	    	{
	    		$('#loginModal').modal({backdrop: 'static', keyboard: false});	    
	    		setTimeout(function(){
					$('#login').focus();
					$("#login:text:visible:first").focus();
				}, 750);		
	    	} else 
	    	{
	    		updtChat();
	    	}
	    });
});

//Submit on Enter everywhere
$(document).ready(function()
{
	//for chat
	$("#msg").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#sendMsg').click();
		}
	});
	//for login
	$("#login").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#pswrdBtn').click();
		}
	});

	$("#pswrd").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#pswrdBtn').click();
		}
	});
	//for registration
	$("#regLog").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#regBtn').click();
		}
	});

	$("#regPswrd").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#regBtn').click();
		}
	});

	$("#regConf").keydown(function(event)
	{
		if(event.keyCode == 13)
		{
		  event.preventDefault();
		  $('#regBtn').click();
		}
	});
});

//login form handler
$(document).ready(function()
{
	$('#pswrdBtn').click(function()
	{
		if (($('#login').val() != "") && ($('#pswrd').val() != ""))
		{
			$.getJSON('/_tryLogin',
			{
		        login: $('#login').val(),
		        password: $('#pswrd').val()
		    }, function(data)
		    {
		    	if (data.nsfw == "SUCC")
		    	{
		    		$('#loginModal').modal('toggle');
		    		updtChat();
		    	}else if (data.nsfw == "LOG")
		    	{
		    		$('#login').val('');
		    		$("#login").attr("placeholder", "incorrect login");
		    	}else if (data.nsfw == "PASS")
		    	{
		    		$('#pswrd').val('');
		    		$("#pswrd").attr("placeholder", "incorrect password");
		    	}
		    });
		}
	});
	$('#register').click(function()
	{
		$('#loginModal').modal('toggle');
		$('#regModal').modal({backdrop: 'static', keyboard: false});
		setTimeout(function(){
			$('#regLog').focus();
			$("#regLog:text:visible:first").focus();
		}, 750);
	});
});

//registration form handler
$(document).ready(function(){
	$('#regBtn').click(function()
	{
		if (($('#regLog').val() != "") && ($('#regPswrd').val() != "") && ($('#regConf').val() != ""))
		{
			if ($('#regPswrd').val() == $('#regConf').val())
			{
				$.getJSON('/_register',
				{
			        login: $('#regLog').val(),
			        password: $('#regPswrd').val()
			    }, function(data)
			    {
			    	if (data.nsfw == "SUCC")
			    	{
			    		$('#regModal').modal('toggle');
			    		updtChat();
			    	}else if (data.nsfw == "LOG")
			    	{
			     		$('#regLog').val('');
			    		$("#regLog").attr("placeholder", "incorrect login");
			    	}
		    	});
			} else
			{
				$('#regPswrd').val('');
				$('#regConf').val('');
			    $("#regConf").attr("placeholder", "passwords don't match");
			}
		}
	});

	$('#regClose').click(function()
	{
		$('#regModal').modal('toggle');
		$('#loginModal').modal({backdrop: 'static', keyboard: false});
	});
});

//sends chatbox's msg
function sendChat()
{
	var msg = $('#msg').val();
	if (msg != '')
	{
		//GET request using JSON as message format
		$.getJSON('/_sendMessage', {
	        msg: $('#msg').val()
	    });
	    $('#msg').val('');
	    return false;
	}
}

//fetches new msgs from server, then requests it again
function updtChat()
{
	$.getJSON('/_updtChat', 
	{
		async:true,
	}, function(data) 
    {
    	if (data.nsfw != "KOK")
    	{
    		var chatArea = document.getElementById('chat-area');
    		console.log($('#chat-area').height());
     		if (chatArea.scrollHeight <= (chatArea.scrollTop + $('#chat-area').height()) + 14)
     		{     
     		    $('#chat-area').val($('#chat-area').val() + data.nsfw);     						     		
				chatArea.scrollTop = chatArea.scrollHeight;
     		} else
     		{
     			$('#chat-area').val($('#chat-area').val() + data.nsfw); 
     		}
     		updtChat();
     		return false;
    	} else 
    	{
    		updtChat();
    		return false;
    	}
	});
}

//Open chat. Duh.
function openChat()
{
	$(':focus').blur();
	$('#chatModal').modal({backdrop: 'static'});
	setTimeout(function(){
		var chatArea = document.getElementById('chat-area');
		chatArea.scrollTop = chatArea.scrollHeight;
	}, 200);
	setTimeout(function(){
		$('#msg').focus();
		$("#msg:text:visible:first").focus();
	}, 550);
}

//logout and refreshing page. Ubelievable
function logout()
{
	$.getJSON('/_logout', 
		{}, function(data){});
	$('#logoutBtn').prop('disabled', true);
	window.location.reload();
}
