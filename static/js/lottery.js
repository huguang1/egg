
	var win_height = 0;
	var prizeNum = 0;
	var prizeArr = [36,72,108,144,180,216,252,288,324,360];

	var resultId = '';
	var resultMsg = '';

	var bRotate = false;
	var bCode = '';
        var bInfo = false;	

	$(function (){
		

		//消息窗
		function msgBox(_title, _content){
			$('#msgBox').show();
			$('#msg_html').html(_content);
		}
			
		//中奖查询
        $('.queryBox').on('click', function(event){
            event.preventDefault();
            $('#queryBox').show();
        });
		
		
		
		lotterylist();



		//砸蛋事件
		$('.egg').click(function (){

//			if(bRotate || bInfo)return;			
//			bInfo = !bInfo;
			$.ajax({
				url: '/lottery/info',
				dataType: 'json',
				cache: false,
				type: 'POST',
				data: {
					bonuscode: bCode,
					csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()
				},
				success: function(obj) {
					switch (obj.stat) {
					case '-1':
						logBox();
//	                        bInfo = !bInfo;
						break;
					case '-3':
						msgBox('温馨提示', '您的会员账号已经没有抽奖机会了!');
						bCode = "";
//						bInfo = !bInfo;
						break;
					case '5':
						msgBox('温馨提示', obj.msg);
//						bInfo = !bInfo;
						break;
					case '0':
					
						$('#awardBox').show();
						if(obj.pId == 11){
							$('.pop_no_award').show();
							$('.pop_award').hide();
						}
						else {
							$('.pop_no_award').hide();
							$('.pop_award').show();
							var prizeUrl = "../static/images/"+obj.pId+".png";
							console.log(prizeUrl);
							$('.pop_award_money').attr("src", prizeUrl);
						}

						
//						rotateFn(resultPid, prizeArr[resultPid], resultMsg);
//						bInfo = !bInfo;
						break;
					default:
						msgBox('温馨提示', obj.msg);
//						bInfo = !bInfo;
						break
					}
				},
				failure: function() {},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					msgBox('温馨提示', '网络错误,请稍后再抽奖')
				}
			})
		});
	});
	
	

//	function rotateFn(awards, angles, txt){
//		bRotate = !bRotate;
//		$('#dzp_img').stopRotate();
//		$('#dzp_img').rotate({
//				angle:0,
//				animateTo:angles+1800,
//				duration:8000,
//				callback:function (){
//					msgBox('温馨提示',txt);
//					bRotate = !bRotate;
//			}
//		})
//	};

    function login(){
    			var _bonuscode = $("#login-na").val();
				if (_bonuscode == "") {
					alert("会员账号不能为空!");
					return false;
				}
				bCode = _bonuscode;
				var _obj = this;
				$.ajax({
					url: '/lottery/verify',
					dataType: 'json',
					cache: false,
					type: 'POST',
					data: {
						bonuscode: bCode,
						csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()
					},
					success: function(obj) {
						switch (obj.stat) {
						case '-1':
							alert('您输入的会员账号不能为空!');
							break;
						case '-2':
							alert('尊敬的会员：您好，您的会员账号不符合抽奖条件，请您查看下方的抽奖规则，或者联系在线客服咨询即可，谢谢~');
							break;
						case '0':
							alert("验证成功,您还有"+obj.score+"次抽奖机会! \r\n赶快来砸幸运金蛋吧!");
							$(".tanshow").hide();
							break;
						default:
							alert('网络错误,请稍后再抽奖');
							break
						}
					},
					error: function(XMLHttpRequest, textStatus, errorThrown) {
						var x = 1
					}
				});
    	
    }

	function logBox() {
		$("#logBox").show();
	}



	//滚动的中奖名单
	function lotterylist(){
		$.ajax({
			url: '/lottery/records',
			dataType: 'json',
			cache: false,
			type: 'POST',
			data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val()},
			success: function (obj) {       
				if(obj){
					var sAwardEle = "";
					$.each(obj, function(i, award){						
						sAwardEle += '<li>恭喜 '+award.user+' 获得 '+award.prize+'</li>';
					});
                  
					$("#lottery_list").html(sAwardEle);                            
					$(".listul").myScroll({
                      speed:60,
                      rowHeight:26
                    });
				}              
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				var x = 1;
              console.log(11)
			}
		}) 
	}
	
	
	
	
function queryBtn(){
		
		var _bonuscode = $("#querycode").val();

		if(_bonuscode == ""){

			alert("输入会员账号不能为空!");

			return false;

		}

		queryPage(1);
		
	}

var pagesize = 5;



function queryPage(page){

				$.ajax({

					url: '/lottery/records/mine?action=querylist&p='+page+'&size='+pagesize,

					dataType: 'json',

					cache: false,

					data : {querycode:$("#querycode").val()},

					type: 'GET',

					success: function (obj) {

						if(obj.count != 0){

							var sHtml1 = "";
							
							var x = "";

							$.each(obj.data, function(i, award){

								x = (award.is_send == 1)?"<font style='color:#065a1d;'>已派彩</font>":"<font style='color:#ec0000;'>未派彩</font>";
							
							    sHtml1 +="<tr><td>"+award.prize_name+"</td><td>"+award.win_time+"</td><td>"+x+"</td></tr>";

							})

							var sPage = Paging(page,pagesize,obj.count,2,"queryPage",'cur','','上一页','下一页');

							$(".page").html(sPage);							

							$("#query_content").html(sHtml1);

						}else{

							$("#query_content").html("<tr><td colspan='3'>未找到相关信息</td></tr>");

						}

					},

					error: function(XMLHttpRequest, textStatus, errorThrown) {

						var x = 1;

					}

				})

} 

	
function Paging(pageNum,pageSize,totalCount,skipCount,fuctionName,currentStyleName,currentUseLink,preText,nextText,firstText,lastText){

	    var returnValue = "";

	    var begin = 1;

	    var end = 1;

	    var totalpage = Math.floor(totalCount / pageSize);

	    if(totalCount % pageSize >0){

	        totalpage ++;

	    }	   

	    if(preText == null){

	        firstText = "prev";

	    }

	    if(nextText == null){

	        nextText = "next";

	    }

	    

	    begin = pageNum - skipCount;

	    end = pageNum + skipCount;

	    

	    if(begin <= 0){

	        end = end - begin +1;

	        begin = 1;

	    }

	    

	    if(end > totalpage){

	        end = totalpage;

	    }

	    for(count = begin;count <= end;count ++){

	        if(currentUseLink){ 

	            if(count == pageNum){

	                returnValue += "<a class=\""+currentStyleName+"\" href=\"javascript:void(0);\" onclick=\""+fuctionName+"("+count.toString()+");\">"+count.toString()+"</a> ";

	            }

	            else{

	                returnValue += "<a href=\"javascript:void(0);\" onclick=\"" + fuctionName + "(" + count.toString() + ");\">" + count.toString() + "</a> ";

	            }

	        }

	        else {

	            if (count == pageNum) {

	                returnValue += "<span class=\""+currentStyleName+"\">"+count.toString()+"</span> ";

	            }

	            else{           

	                returnValue += "<a href=\"javascript:void(0);\" onclick=\""+fuctionName+"("+count.toString()+");\">"+count.toString()+"</a> ";}

	            }

	        }

	        if(pageNum - skipCount >1){

	            returnValue = " ... "+returnValue;

	        }

	        if(pageNum + skipCount < totalpage){

	            returnValue = returnValue + " ... ";

	        }

	        

	        if(pageNum > 1){

	            returnValue = "<a href=\"javascript:void(0);\" onclick=\""+fuctionName+"("+(pageNum - 1).toString()+");\"> " + preText + "</a> " + returnValue;

	        }

	        if(pageNum < totalpage){

	            returnValue = returnValue + " <a href=\"javascript:void(0);\" onclick=\""+fuctionName+"("+(pageNum+1).toString()+");\">" + nextText + "</a>";

	        }

	        

	        if(firstText!= null){

	            if(pageNum >1){

	                returnValue = "<a href=\"javascript:void(0);\" onclick=\""+fuctionName+"(1);\">" + firstText + "</a> " + returnValue;}

	        }

	        if(lastText !=null){

	            if(pageNum < totalpage){

	                returnValue = returnValue + " " + " <a href=\"javascript:void(0);\" onclick=\""+fuctionName+"("+totalpage.toString()+");\">" + lastText + "</a>";}

	        }

	        return returnValue;

        

	}
