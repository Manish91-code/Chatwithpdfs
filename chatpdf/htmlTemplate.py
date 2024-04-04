css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/png;base64,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">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.google.com/imgres?q=male%20human%20with%20clothes%20face&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F519543349%2Fphoto%2Fyoung-mans-face.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3Dyx1LFKdibOL6RBmcDBC4Ks3Ygok1weaVfql0TpCyH_M%3D&imgrefurl=https%3A%2F%2Fdesignco-india.com%2Frevsliderl%2FFace-Stock-Photo-Download-Image-Now-Serious-Men-Human-Face-3127881.html&docid=952u2MaNWkHEiM&tbnid=1s5luTaMxt5CJM&vet=12ahUKEwih7cPBpaCFAxXq-jgGHUyvC-kQM3oECFsQAA..i&w=612&h=406&hcb=2&ved=2ahUKEwih7cPBpaCFAxXq-jgGHUyvC-kQM3oECFsQAA">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''