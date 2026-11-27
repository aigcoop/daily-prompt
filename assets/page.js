(function(){
  function run(btn){
    var id=btn.getAttribute('data-copy'),box=document.getElementById(id),
        msg=document.getElementById('m-'+id),label=btn.getAttribute('data-label');
    function done(){btn.textContent='복사됐어요';msg.textContent='이제 대화창에 붙여넣기 하세요.';
      setTimeout(function(){btn.textContent=label},2500)}
    function fallback(){
      try{
        var r=document.createRange();r.selectNodeContents(box);
        var s=window.getSelection();s.removeAllRanges();s.addRange(r);
        if(document.execCommand('copy')){done()}
        else{msg.textContent='글이 선택됐어요. 길게 눌러 복사를 눌러 주세요.'}
      }catch(e){msg.textContent='프롬프트 글을 길게 눌러 복사해 주세요.'}
    }
    var t=box.textContent;
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(t).then(done).catch(fallback);
    }else{fallback()}
  }
  var bs=document.querySelectorAll('button[data-copy]');
  for(var i=0;i<bs.length;i++){bs[i].addEventListener('click',function(){run(this)})}
})();
