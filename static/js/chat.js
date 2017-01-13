//Call login modal on page's load
$(window).ready(function()
{
    $('#loginModal').modal({backdrop: 'static', keyboard: false});
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
		  sendChat();
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
//			    		setInterval(updtChat(), 1000);
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

function updtChat()
{
	$.getJSON('/_updtChat', 
	{}, function(data) 
    {
    	if (data.nsfw == "SUCC")
    	{
    		//TODO
    	}else
    	{
     		$('#chat-area').val($('#chat-area').val() + data.nsfw);
    	}
	});	
}

function openChat() 
{
	$('#chatModal').modal({backdrop: 'static'});
}
