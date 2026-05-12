from flask import Flask,render_template,redirect,url_for,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime,date,timedelta;import time;import threading
import uuid;import base64;

#--------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.secret_key = 'secret_key'

#--------------------------------------#

class Admins(db.Model):
    id = db.Column(db.String,primary_key = True)
    admin_name = db.Column(db.String,nullable = False)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,unique = True,nullable = False)
    is_authenticated = db.Column(db.Boolean,default = False,nullable = False)
    is_active = db.Column(db.Boolean,default = True,nullable = False)

    def get_id(self):
        return str(self.id)

#--------------------------------------#

class Sponsors(db.Model):
    id = db.Column(db.String,primary_key = True)
    sponsor_name = db.Column(db.String,nullable = False)
    industry = db.Column(db.String,nullable = False)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,unique = True,nullable = False)
    flagged = db.Column(db.Boolean,default = False,nullable = False)
    campaigns = db.relationship('Campaigns',backref = 'sponsor',cascade = "all, delete")
    requests = db.relationship('Requests',backref = 'sponsor',cascade = "all, delete")
    negotiaton_requests = db.relationship('Negotiation_Requests',backref='sponsor',cascade='all, delete')
    is_authenticated = db.Column(db.Boolean,default = False,nullable = False)
    is_active = db.Column(db.Boolean,default = True,nullable = False)

    def get_id(self):
        return str(self.id)

#--------------------------------------#   
    
class Influencers(db.Model):
    id = db.Column(db.String,primary_key = True)
    influencer_name = db.Column(db.String,nullable = False)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)
    email = db.Column(db.String,unique = True,nullable = False)
    niche = db.Column(db.String,nullable = False)
    followers = db.Column(db.String,nullable = False)
    flagged = db.Column(db.Boolean,default = False,nullable = False)
    requests = db.relationship('Requests',backref = 'influencer',cascade = "all, delete")
    negotiaton_requests = db.relationship('Negotiation_Requests',backref='influencer',cascade='all, delete')
    is_authenticated = db.Column(db.Boolean,default = False,nullable = False)
    is_active = db.Column(db.Boolean,default = True,nullable = False)

    def get_id(self):
        return str(self.id)

#--------------------------------------#    

class Campaigns(db.Model):
    campaign_id = db.Column(db.String,primary_key = True)
    sponsor_id = db.Column(db.String,db.ForeignKey('sponsors.id',ondelete = 'CASCADE'),nullable = False)
    campaign_name = db.Column(db.String,nullable = False)
    campaign_field = db.Column(db.String,nullable = False)
    goal = db.Column(db.String,nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    budget = db.Column(db.Integer,nullable = False)
    visibility = db.Column(db.String,nullable = False)
    status = db.Column(db.String,nullable = False,default = 'Active')
    flagged = db.Column(db.Boolean,default = False,nullable = False)
    requests = db.relationship('Requests',backref='campaign',cascade='all, delete')
    negotiaton_requests = db.relationship('Negotiation_Requests',backref='campaign',cascade='all, delete')

#--------------------------------------#

class Requests(db.Model):
    request_id = db.Column(db.String,primary_key = True)
    influencer_id = db.Column(db.String,db.ForeignKey('influencers.id',ondelete = 'CASCADE'),nullable = True)
    campaign_id = db.Column(db.String,db.ForeignKey('campaigns.campaign_id',ondelete = 'CASCADE'),nullable = False)
    sponsor_id = db.Column(db.String,db.ForeignKey('sponsors.id',ondelete = 'CASCADE'),nullable = False)
    additional_notes = db.Column(db.String,nullable = False)
    requirements = db.Column(db.String,nullable = False)
    payment_amount = db.Column(db.Integer,nullable = False)
    status = db.Column(db.String,nullable = False,default = 'Pending')
    flagged = db.Column(db.Boolean,default = False,nullable = False)
    negotiaton_requests = db.relationship('Negotiation_Requests',backref='request',cascade='all, delete')
    
#--------------------------------------#

class Negotiation_Requests(db.Model):
    negotiation_id = db.Column(db.String,primary_key = True)
    request_id = db.Column(db.String,db.ForeignKey('requests.request_id',ondelete = 'CASCADE'),nullable = False)
    influencer_id = db.Column(db.String,db.ForeignKey('influencers.id',ondelete = 'CASCADE'),nullable = False)
    sponsor_id = sponsor_id = db.Column(db.String,db.ForeignKey('sponsors.id',ondelete = 'CASCADE'),nullable = False)
    campaign_id = db.Column(db.String,db.ForeignKey('campaigns.campaign_id',ondelete = 'CASCADE'),nullable = False)
    desired_amount = db.Column(db.Integer,nullable = False)
    status = db.Column(db.String,nullable = False,default = 'Pending')
    flagged = db.Column(db.Boolean,default = False,nullable = False)

#--------------------------------------#

class Rejection_bin(db.Model):
    unique_id = db.Column(db.String,primary_key = True)
    request_id = db.Column(db.String,db.ForeignKey('requests.request_id'),nullable = False)
    influencer_id = db.Column(db.String,db.ForeignKey('influencers.id'),nullable = False)

#--------------------------------------#

class Images_Sponsor(db.Model):
    image_id = db.Column(db.String,primary_key = True)
    image_name = db.Column(db.String,nullable = False)
    image_encoding = db.Column(db.String,nullable = False)
    user_id = db.Column(db.String,db.ForeignKey('sponsors.id',ondelete = 'CASCADE'),nullable = False)

#--------------------------------------#

class Images_Influencer(db.Model):
    image_id = db.Column(db.String,primary_key = True)
    image_name = db.Column(db.String,nullable = False)
    image_encoding = db.Column(db.String,nullable = False)
    user_id = db.Column(db.String,db.ForeignKey('influencers.id',ondelete = 'CASCADE'),nullable = False)

#--------------------------------------#

@login_manager.user_loader
def load_user(user_id):
    if((user_id).startswith('adm')):
        return db.session.query(Admins).get(user_id)
    elif((user_id).startswith('spn')):
        return db.session.query(Sponsors).get(user_id)
    elif((user_id).startswith('inf')):
        return db.session.query(Influencers).get(user_id)
    else:
        return None

#--------------------------------------#

@app.route('/',methods = ['GET'])
def home():
    return render_template('home.html',message = request.args.get('message'))

#--------------------------------------#

@app.route('/login_admin',methods = ['GET','POST'])
def login_admin():
    if(request.method == 'GET'): 
        return render_template('login_admin.html',message = '')
    else:
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')
        user = db.session.query(Admins).filter_by(username = admin_username).first()
        if(user):
            if(user.password == admin_password):
                user.is_authenticated = True
                db.session.commit()
                login_user(user)
                return redirect(url_for('dashboard_admin'))
            else:
                return render_template('login_admin.html',message = 'incorrect password !')
        else:
            return render_template('login_admin.html',message = 'username not found !')



@app.route('/dashboard_admin',methods = ['GET','POST'])
@login_required
def dashboard_admin():
    if(current_user.id.startswith('adm')):
        if(request.args.get('message') is None):
            campaigns = db.session.query(Campaigns).all()
            requests = db.session.query(Requests,Influencers,Campaigns,Sponsors).outerjoin(Influencers,Requests.influencer_id == Influencers.id).join(Campaigns).join(Sponsors).filter(Requests.campaign_id == Campaigns.campaign_id,Requests.sponsor_id == Sponsors.id,Campaigns.sponsor_id == Sponsors.id).all()
            sponsors = db.session.query(Sponsors,Images_Sponsor).outerjoin(Images_Sponsor,Sponsors.id == Images_Sponsor.user_id).all()
            influencers = db.session.query(Influencers,Images_Influencer).outerjoin(Images_Influencer,Influencers.id == Images_Influencer.user_id).all()
            negotiation_requests = db.session.query(Negotiation_Requests,Influencers,Sponsors).join(Influencers,Negotiation_Requests.influencer_id == Influencers.id).join(Sponsors,Negotiation_Requests.sponsor_id == Sponsors.id).all()
            return render_template('dashboard_admin.html',message= 'logged in successfully !',user = current_user,campaigns = campaigns,requests = requests,sponsors = sponsors,influencers = influencers,negotiation_requests = negotiation_requests)
        elif(request.args.get('message') == 'null'):
            campaigns = db.session.query(Campaigns).all()
            requests = db.session.query(Requests,Influencers,Campaigns,Sponsors).outerjoin(Influencers,Requests.influencer_id == Influencers.id).join(Campaigns).join(Sponsors).filter(Requests.campaign_id == Campaigns.campaign_id,Requests.sponsor_id == Sponsors.id,Campaigns.sponsor_id == Sponsors.id).all()
            sponsors = db.session.query(Sponsors,Images_Sponsor).outerjoin(Images_Sponsor,Sponsors.id == Images_Sponsor.user_id).all()
            influencers = db.session.query(Influencers,Images_Influencer).outerjoin(Images_Influencer,Influencers.id == Images_Influencer.user_id).all()
            negotiation_requests = db.session.query(Negotiation_Requests,Influencers,Sponsors).join(Influencers,Negotiation_Requests.influencer_id == Influencers.id).join(Sponsors,Negotiation_Requests.sponsor_id == Sponsors.id).all()
            return render_template('dashboard_admin.html',message = '',user = current_user,campaigns = campaigns,requests = requests,sponsors = sponsors,influencers = influencers,negotiation_requests = negotiation_requests)
        else:
            campaigns = db.session.query(Campaigns).all()
            requests = db.session.query(Requests,Influencers,Campaigns,Sponsors).outerjoin(Influencers,Requests.influencer_id == Influencers.id).join(Campaigns).join(Sponsors).filter(Requests.campaign_id == Campaigns.campaign_id,Requests.sponsor_id == Sponsors.id,Campaigns.sponsor_id == Sponsors.id).all()
            sponsors = db.session.query(Sponsors,Images_Sponsor).outerjoin(Images_Sponsor,Sponsors.id == Images_Sponsor.user_id).all()
            influencers = db.session.query(Influencers,Images_Influencer).outerjoin(Images_Influencer,Influencers.id == Images_Influencer.user_id).all()
            negotiation_requests = db.session.query(Negotiation_Requests,Influencers,Sponsors).join(Influencers,Negotiation_Requests.influencer_id == Influencers.id).join(Sponsors,Negotiation_Requests.sponsor_id == Sponsors.id).all()
            return render_template('dashboard_admin.html',message= request.args.get('message'),user = current_user,campaigns = campaigns,requests = requests,sponsors = sponsors,influencers = influencers,negotiation_requests = negotiation_requests)  
    else:
        return render_template('unauthorized_access.html')



@app.route('/data_stats/<data_type>',methods = ['GET'])
@login_required
def data_stats(data_type):
    if(current_user.id.startswith('adm')):
        if(data_type == 'inf_distr_data'):
            data = db.session.query(Influencers,func.count(Influencers.id).label('count')).group_by(Influencers.niche).order_by(Influencers.niche).all()
            data = {f'{record[0].niche}': record[1] if record[1] > 0 else 0 for record in data}
            return jsonify(data)
        
        elif(data_type == 'flagged_infs_data'):
            data = db.session.query(Influencers.flagged,func.count(Influencers.id).label('count')).group_by(Influencers.flagged).order_by(Influencers.flagged).all()
            if(not data):
                return jsonify({'False' : 0,'True' : 0})
            inf_count = db.session.query(Influencers).count()
            if(len(data) == 1 and data[0][0] == False):
                data = [data[0][1],inf_count - data[0][1]]
            elif(len(data) == 1 and data[0][0] == True):
                data = [inf_count - data[0][1],data[0][1]]
            else:
                data = [data[0][1],data[1][1]]
            return jsonify(data)
        
        elif(data_type == 'spn_distr_data'):
            data = db.session.query(Sponsors,func.count(Sponsors.id).label('count')).group_by(Sponsors.industry).order_by(Sponsors.industry).all()
            data = {f'{record[0].industry}': record[1] if record[1] > 0 else 0 for record in data}
            return jsonify(data)
        
        elif(data_type == 'flagged_spns_data'):
            data = db.session.query(Sponsors.flagged,func.count(Sponsors.id).label('count')).group_by(Sponsors.flagged).order_by(Sponsors.flagged).all()
            spn_count = db.session.query(Sponsors).count()
            if(not data):
                return jsonify({'False' : 0,'True' : 0})
            if(len(data) == 1 and data[0][0] == False):
                data = [data[0][1],spn_count - data[0][1]]
            elif(len(data) == 1 and data[0][0] == True):
                data = [data[0][1],spn_count - data[0][1]]
            else:
                data = [data[0][1],data[1][1]]
            return jsonify(data)
        
        elif(data_type == 'req_distr_data'):
            data = db.session.query(Requests,Campaigns,func.count(Requests.request_id).label('count')).join(Campaigns,Requests.campaign_id == Campaigns.campaign_id).group_by(Campaigns.campaign_field).order_by(Campaigns.campaign_field).all()
            data = {f'{record[1].campaign_field}': record[2] if record[2] > 0 else 0 for record in data}
            return jsonify(data)
        
        elif(data_type == 'flagged_reqs_data'):
            data = db.session.query(Requests.flagged,func.count(Requests.request_id).label('count')).group_by(Requests.flagged).order_by(Requests.flagged).all()
            req_count = db.session.query(Requests).count()
            if(not data):
                return jsonify({'False' : 0,'True' : 0})
            if(len(data) == 1 and data[0][0] == False):
                data = [data[0][1],req_count - data[0][1]]
            elif(len(data) == 1 and data[0][0] == True):
                data = [data[0][1],req_count - data[0][1]]
            else:
                data = [data[0][1],data[1][1]]
            return jsonify(data)
        
        elif(data_type == 'camp_distr_data'):
            data = db.session.query(Campaigns,func.count(Campaigns.campaign_id).label('count')).group_by(Campaigns.campaign_field).order_by(Campaigns.campaign_field).all()
            data = {f'{record[0].campaign_field}': record[1] if record[1] > 0 else 0 for record in data}
            return jsonify(data)
        
        elif(data_type == 'flagged_camps_data'):
            data = db.session.query(Campaigns.flagged,func.count(Campaigns.campaign_id).label('count')).group_by(Campaigns.flagged).order_by(Campaigns.flagged).all()
            camp_count = db.session.query(Campaigns).count()
            if(not data):
                return jsonify({'False' : 0,'True' : 0})
            if(len(data) == 1 and data[0][0] == False):
                data = [data[0][1],camp_count - data[0][1]]
            elif(len(data) == 1 and data[0][0] == True):
                data = [data[0][1],camp_count - data[0][1]]
            else:
                data = [data[0][1],data[1][1]]
            return jsonify(data)
    else:
        return render_template('unauthorized_access.html')


@app.route('/statistics',methods = ['GET'])
@login_required
def statistics():
    if(current_user.id.startswith('adm')):
        return render_template('statistics.html')
    else:
        return render_template('unauthorized-access.html')



@app.route('/flag',methods=['GET'])
@login_required
def flag():
    if(current_user.id.startswith('adm')):
        if(list(request.args) == ['sponsor_id']):
            sponsor = db.session.query(Sponsors).filter_by(id = request.args.get('sponsor_id')).first()
            sponsor.flagged = True
            sponsor.is_authenticated = False
            campaigns = db.session.query(Campaigns).filter_by(sponsor_id = request.args.get('sponsor_id')).all()
            for campaign in campaigns:
                campaign.flagged = True;campaign.status = 'N/A'
                requests = db.session.query(Requests).filter_by(campaign_id = campaign.campaign_id).all()
                for current_request in requests:
                    current_request.flagged = True;current_request.status = 'N/A'
                    negotiation_requests = db.session.query(Negotiation_Requests).filter_by(request_id = current_request.request_id).all()
                    for negotiation_request in negotiation_requests:
                        negotiation_request.status = 'N/A'
            db.session.commit()
            return redirect(url_for('dashboard_admin',message = 'sponsor flagged successfully !'))
        
        elif(list(request.args) == ['influencer_id']):
            influencer = db.session.query(Influencers).filter_by(id = request.args.get('influencer_id')).first()
            influencer.flagged = True
            influencer.is_authenticated = False
            negotiation_requests = db.session.query(Negotiation_Requests).filter_by(influencer_id = influencer.id).all()
            for negotiation_request in negotiation_requests:
                negotiation_request.flagged = True
                ad_request,parent_campaign = db.session.query(Requests,Campaigns).filter(Requests.request_id == negotiation_request.request_id,Campaigns.campaign_id == Requests.campaign_id).first()
                if(negotiation_request.status == 'Accepted'):
                    ad_request.status = 'Pending'
                    if(parent_campaign.campaign_id.startswith('pbl')):
                        ad_request.influencer_id = None
                        ad_request.payment_amount = 10000
                    elif(parent_campaign.campaign_id.startswith('pvt')):
                        ad_request.payment_amount = 10000
                negotiation_request.status = 'N/A'
            db.session.commit()
            return redirect(url_for('dashboard_admin',message = 'influencer flagged successfully !'))
        
        elif(list(request.args) == ['campaign_id']):
            campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first()
            campaign.flagged = True;campaign.status = 'N/A'
            requests = db.session.query(Requests).filter_by(campaign_id = campaign.campaign_id).all()
            for current_request in requests:
                current_request.flagged = True;current_request.status = 'N/A'
                negotiation_requests = db.session.query(Negotiation_Requests).filter_by(request_id = current_request.request_id).all()
                for negotiation_request in negotiation_requests:
                    negotiation_request.status = 'N/A' 
            db.session.commit()
            return redirect(url_for('dashboard_admin',message = 'campaign flagged successfully !'))
        
        elif(list(request.args) == ['request_id']):
            flag_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first()
            flag_request.flagged = True;flag_request.status = 'N/A'
            negotiation_requests = db.session.query(Negotiation_Requests).filter_by(request_id = request.args.get('request_id')).all()
            for negotiation_request in negotiation_requests:
               negotiation_request.status = 'N/A'
            db.session.commit()
            return redirect(url_for('dashboard_admin',message = 'request flagged successfully !'))
        
        elif(list(request.args) == ['negotiation_id']):
            negotiation = db.session.query(Negotiation_Requests).filter_by(negotiation_id = request.args.get('negotiation_id')).first()
            negotiation.flagged = True
            ad_request,parent_campaign = db.session.query(Requests,Campaigns).filter(Requests.request_id == negotiation.request_id,Campaigns.campaign_id == Requests.campaign_id).first()
            if(negotiation.status == 'Accepted'):
                ad_request.status = 'Pending'
                if(parent_campaign.campaign_id.startswith('pbl')):
                    ad_request.influencer_id = None
                    ad_request.payment_amount = 10000
                elif(parent_campaign.campaign_id.startswith('pvt')):
                    ad_request.payment_amount = 10000
            negotiation.status = 'N/A'
            db.session.commit()
            return redirect(url_for('dashboard_admin',message = 'negotiation request flagged successfully !'))
    else:
        return render_template('unauthorized_access.html')

#--------------------------------------#

@app.route('/login_influencer',methods = ['GET','POST'])
def login_influencer():
    if(request.method == 'GET'): 
        return render_template('login_influencer.html',message = '')
    else:
        influencer_username = request.form.get('username')
        influencer_password = request.form.get('password')
        user = db.session.query(Influencers).filter_by(username = influencer_username).first()
        if(user):
            if(user.password == influencer_password):
                if(not user.flagged):
                    user.is_authenticated = True
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('dashboard_influencer'))
                else:
                    return render_template('login_influencer.html',message = 'influencer flagged !')
            else:
                return render_template('login_influencer.html',message = 'incorrect password !')
        else:
            return render_template('login_influencer.html',message = 'username not found !')



@app.route('/create_influencer',methods = ['GET','POST'])
def create_influencer():
    if(request.method == 'GET'):
        return render_template('create_influencer.html',message =  '')
    else:
        data = request.form
        try:
            new_influencer = Influencers(id = ('inf'+f'{uuid.uuid4()}')[:10],influencer_name = data['name'],email = data['email'],username = data['username'],password = data['password'],niche = data['niche'],followers = data['follower_count'])
            db.session.add(new_influencer)
            db.session.commit()
            return render_template('create_influencer.html',message = 'influencer account created !')
        except IntegrityError:
            return render_template('create_influencer.html',message = 'enter unique username/email address !')



@app.route('/dashboard_influencer',methods = ['GET'])
@login_required
def dashboard_influencer():
    if(current_user.id.startswith('inf')):
        if(list(request.args) == []):
            return render_template('dashboard_influencer.html',message = 'logged in successfully !',user = current_user)
        elif(list(request.args) == ['message'] and request.args.get('message') == 'null'):
            return render_template('dashboard_influencer.html',message = '',user = current_user)
        elif(sorted(list(request.args)) == ['campaign_field']):
            public_campaigns = db.session.query(Campaigns).filter(Campaigns.visibility == 'Public',Campaigns.campaign_field == request.args.get('campaign_field'),Campaigns.flagged == False,Campaigns.status != 'Completed').all()
            if(public_campaigns):
                return render_template('dashboard_influencer.html',message = '',user = current_user,public_campaigns = public_campaigns,campaign_field = request.args.get('campaign_field'))
            else:
                return render_template('dashboard_influencer.html',message = '',user = current_user,campaign_field = request.args.get('campaign_field'))   
    else:
        return render_template('unauthorized_access.html')
    


@app.route('/requests_undertaken',methods = ['GET'])
@login_required
def requests_undertaken():
    if(current_user.id.startswith('inf')):
        accepted_requests = db.session.query(Requests,Campaigns,Sponsors).filter(Requests.influencer_id == current_user.id,or_(Requests.status == 'Accepted',Requests.status == 'Completed'),Requests.campaign_id == Campaigns.campaign_id,Requests.sponsor_id == Sponsors.id,Requests.flagged == False).all()
        return render_template('requests_undertaken.html',accepted_requests = accepted_requests)
    else:
        return render_template('unauthorized_access.html')



@app.route('/profile_influencer',methods = ['GET','POST'])
@login_required
def profile_influencer():
    if(current_user.id.startswith('inf')):
        if(request.method == 'GET'):
            image_influencer = db.session.query(Images_Influencer).filter_by(user_id = current_user.id).first()
            if(image_influencer):
                return render_template('profile_influencer.html',message = '',user = current_user,image_encoding = image_influencer.image_encoding)
            else:
                return render_template('profile_influencer.html',message = '',user = current_user)
        else:
            image = request.files['image']
            if(image):
                current_image = db.session.query(Images_Influencer).filter_by(user_id = current_user.id).first()
                if(current_image):
                    db.session.delete(current_image)
                    image_data = image.read()
                    image_encoding = base64.b64encode(image_data).decode('utf-8')
                    new_image = Images_Influencer(image_id = f'{ uuid.uuid4()}'[:7],image_name = f'{current_user.influencer_name}_profile_img',image_encoding = image_encoding,user_id = current_user.id)
                    db.session.add(new_image)
                    current_user.influencer_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    current_user.followers = request.form.get('follower_count')
                    db.session.commit()
                    return render_template('profile_influencer.html',image_encoding = image_encoding,user = current_user,message = 'changes saved successfully !')
                else:
                    image_data = image.read()
                    image_encoding = base64.b64encode(image_data).decode('utf-8')
                    new_image = Images_Influencer(image_id = f'{ uuid.uuid4()}'[:7],image_name = f'{current_user.influencer_name}_profile_img',image_encoding = image_encoding,user_id = current_user.id)
                    db.session.add(new_image)
                    current_user.influencer_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    current_user.followers = request.form.get('follower_count')
                    db.session.commit()
                    return render_template('profile_influencer.html',image_encoding = image_encoding,user = current_user,message = 'changes saved successfully !')
            else:
                image_influencer = db.session.query(Images_Influencer).filter_by(user_id = current_user.id).first()
                if(image_influencer):
                    current_user.influencer_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    current_user.followers = request.form.get('follower_count')
                    db.session.commit()
                    return render_template('profile_influencer.html',image_encoding = image_influencer.image_encoding,user = current_user,message = 'changes saved successfully !')
                else:
                    current_user.influencer_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    current_user.followers = request.form.get('follower_count')
                    db.session.commit()
                    return render_template('profile_influencer.html',user = current_user,message = 'changes saved successfully !')
    else:
        return render_template('unauthorized_access.html')



@app.route('/public_requests',methods = ['GET','POST'])
@login_required
def public_requests():
    if(current_user.id.startswith('inf')):
        if(request.args.get('message') is None):
            campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id'),flagged = False,status = 'Active').first()
            campaign_requests = db.session.query(Requests,Sponsors).filter(Requests.campaign_id == campaign.campaign_id,
            or_(Requests.influencer_id == current_user.id,Requests.influencer_id.is_(None)),Requests.flagged == False,Requests.sponsor_id == Sponsors.id).all()
            rejected_requests = db.session.query(Rejection_bin).filter_by(influencer_id = current_user.id).all()
            requests = []
            for campaign_request in campaign_requests:
                check = False
                for rejected_request in rejected_requests:
                    if(campaign_request[0].request_id == rejected_request.request_id):
                        check = True;break
                if(not check):
                    requests.append(campaign_request)
            return render_template('public_requests.html',message = '',campaign = campaign,requests = requests)
        else:
            campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id'),flagged = False,status = 'Active').first()
            campaign_requests = db.session.query(Requests,Sponsors).filter(Requests.campaign_id == campaign.campaign_id,
            or_(Requests.influencer_id == current_user.id, Requests.influencer_id.is_(None)),Requests.flagged == False,Requests.sponsor_id == Sponsors.id).all()
            rejected_requests = db.session.query(Rejection_bin).filter_by(influencer_id = current_user.id).all()
            requests = []
            for campaign_request in campaign_requests:
                check = False
                for rejected_request in rejected_requests:
                    if(campaign_request[0].request_id == rejected_request.request_id):
                        check = True;break
                if(not check):
                    requests.append(campaign_request)
            return render_template('public_requests.html',campaign = campaign,requests = requests,message = request.args.get('message'))
    else:
        return render_template('unauthorized_access.html')
    


@app.route('/negotiations_sent',methods = ['GET'])
@login_required
def negotiations_sent():
    if(current_user.id.startswith('inf')):
          negotiation_requests = db.session.query(Negotiation_Requests,Requests,Campaigns).join(Requests,Negotiation_Requests.request_id == Requests.request_id).join(Campaigns,Campaigns.campaign_id == Negotiation_Requests.campaign_id).filter(Negotiation_Requests.influencer_id == current_user.id,Negotiation_Requests.flagged == False).all()
          return render_template('negotiations_sent.html',negotiation_requests = negotiation_requests)
    else:
        return render_template('unauthorized_access.html')



@app.route('/pvt_requests',methods = ['GET'])
@login_required
def pvt_requests():
    if(current_user.id.startswith('inf')):
        if(request.args.get('message') is None):
            requests = db.session.query(Requests,Campaigns,Sponsors).filter(Requests.influencer_id == current_user.id,Campaigns.visibility == 'Private',Requests.flagged == False,Requests.sponsor_id == Sponsors.id,Requests.campaign_id == Campaigns.campaign_id,Campaigns.sponsor_id == Sponsors.id).all()
            return render_template('pvt_requests.html',requests = requests,message = '')
        else:
            requests = db.session.query(Requests,Campaigns,Sponsors).filter(Requests.influencer_id == current_user.id,Campaigns.visibility == 'Private',Requests.flagged == False,Requests.sponsor_id == Sponsors.id,Requests.campaign_id == Campaigns.campaign_id,Campaigns.sponsor_id == Sponsors.id).all()
            return render_template('pvt_requests.html',requests = requests,message = request.args.get('message'))
    else:
        return render_template('unauthorized_access.html')
    


@app.route('/accept',methods = ['GET'])
@login_required
def accept():
    if(current_user.id.startswith('inf')):
        current_request = db.session.query(Requests).filter(Requests.request_id == request.args.get('request_id'),Requests.flagged == False,Requests.status == 'Pending').first()
        if(not current_request):
            return render_template('invalid_flagged.html',element = "Request")
        negotiation_requests = db.session.query(Negotiation_Requests).filter_by(request_id = current_request.request_id,status = 'Pending').all()
        for negotiation_request in negotiation_requests:
            negotiation_request.status = 'N/A'
            db.session.commit()
        if(request.args.get('type') == 'private'):
            current_request.influencer_id = current_user.id
            current_request.status = 'Accepted'
            db.session.commit()
            return redirect(url_for('pvt_requests',message = 'request accepted successfully !'))
        elif(request.args.get('type') == 'public'):
            current_request.influencer_id = current_user.id
            current_request.status = 'Accepted'
            db.session.commit()
            return redirect(url_for('public_requests',campaign_id = request.args.get('campaign_id'),message = 'request accepted successfully !'))
    else:
       return render_template('unauthorized_access.html')



@app.route('/reject',methods = ['GET'])
@login_required
def reject():
    if(current_user.id.startswith('inf')):
        current_request = db.session.query(Requests).filter(Requests.request_id == request.args.get('request_id'),Requests.flagged == False,Requests.status == 'Pending').first()
        if(not current_request):
            return render_template('invalid_flagged.html',element = "Request")
        if(request.args.get('type') == 'private'):
            current_request.status = 'Rejected'
            db.session.commit()
            return redirect(url_for('pvt_requests',message = 'request rejected successfully !'))
        elif(request.args.get('type') == 'public'):
            db.session.add(Rejection_bin(unique_id = f'{(uuid.uuid4())}'[:7],request_id = request.args.get('request_id'),
            influencer_id = current_user.id))
            db.session.commit()
            return redirect(url_for('public_requests',campaign_id = request.args.get('campaign_id'),message = 'request rejected successfully !'))
    else:
       return render_template('unauthorized_access.html')



@app.route('/negotiate',methods = ['GET'])
@login_required
def negotiation():
    if(current_user.id.startswith('inf')):
        if(sorted(list(request.args)) == ['campaign_id','request_id','sponsor_id']):
            current_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id'),flagged = False,status = 'Pending').first()
            if(current_request):
                return render_template('add_negotiation_request.html',campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),message = '')
            else:
                return render_template('invalid_flagged.html',element = "Request")
        else:
            if(request.args.get('campaign_id') and request.args.get('request_id') and request.args.get('sponsor_id') and request.args.get('desired_amount')):
                negotiation_request = db.session.query(Negotiation_Requests).filter_by(request_id = request.args.get('request_id'),influencer_id = current_user.id,status = 'Pending').all()
                if(negotiation_request):
                    return render_template('add_negotiation_request.html',campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),message = 'negotiation request already in Queue !')
                else:
                    payment_amount = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first().payment_amount
                    if(payment_amount < int(request.args.get('desired_amount'))):
                        new_negotiation_request = Negotiation_Requests(negotiation_id = f'{(uuid.uuid4())}'[:7],campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),influencer_id = current_user.id,desired_amount = int(request.args.get('desired_amount')))
                        db.session.add(new_negotiation_request)
                        db.session.commit()
                        return render_template('add_negotiation_request.html',campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),message = 'negotiation request sent successfully !')
                    else:
                        return render_template('add_negotiation_request.html',campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),message = 'desired amount must be greater than offered amount !')
            else:
                return render_template('add_negotiation_request.html',campaign_id = request.args.get('campaign_id'),request_id = request.args.get('request_id'),sponsor_id = request.args.get('sponsor_id'),message = 'input fields empty !')
    else:
        return render_template('unauthorized_access.html')

#--------------------------------------#

@app.route('/login_sponsor',methods = ['GET','POST'])
def login_sponsor():
    if(request.method == 'GET'): 
        return render_template('login_sponsor.html',message = '')
    else:
        sponsor_username = request.form.get('username')
        sponsor_password = request.form.get('password')
        user = db.session.query(Sponsors).filter_by(username = sponsor_username).first()
        if(user):
            if(user.password == sponsor_password):
                if(not user.flagged):
                    user.is_authenticated = True
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('dashboard_sponsor'))
                else:
                    return render_template('login_sponsor.html',message = 'sponsor flagged !')  
            else:
                return render_template('login_sponsor.html',message = 'incorrect password !')
        else:
            return render_template('login_sponsor.html',message = 'username not found !')



@app.route('/create_sponsor',methods = ['GET','POST'])
def create_sponsor():
    if(request.method == 'GET'):
        return render_template('create_sponsor.html',message =  '')
    else:
        data = request.form
        try:
            new_sponsor = Sponsors(id = ('spn'+f'{uuid.uuid4()}')[:10],sponsor_name = data['name'],email = data['email'],username = data['username'],password = data['password'],industry = data['industry'])
            db.session.add(new_sponsor)
            db.session.commit()
            return render_template('create_sponsor.html',message = 'sponsor account created !')
        except IntegrityError:
            return render_template('create_sponsor.html',message = 'enter unique username/email address !')



@app.route('/dashboard_sponsor',methods = ['GET'])
@login_required
def dashboard_sponsor():
    if(current_user.id.startswith('spn')):
        if(request.args.get('message') is None):
            campaigns = db.session.query(Campaigns).filter(Campaigns.sponsor_id == current_user.id,Campaigns.flagged == False,Campaigns.status != 'Completed').all()
            return render_template('dashboard_sponsor.html',message = 'logged in successfully !',user = current_user,campaigns = campaigns)
        elif(request.args.get('message') == 'null'):
            campaigns = db.session.query(Campaigns).filter(Campaigns.sponsor_id == current_user.id,Campaigns.flagged == False,Campaigns.status != 'Completed').all()
            return render_template('dashboard_sponsor.html',message = '',user = current_user,campaigns = campaigns)
        else:
            campaigns = db.session.query(Campaigns).filter(Campaigns.sponsor_id == current_user.id,Campaigns.flagged == False,Campaigns.status != 'Completed').all()
            return render_template('dashboard_sponsor.html',message = request.args.get('message'),user = current_user,campaigns = campaigns)
    else:
        return render_template('unauthorized_access.html')



@app.route('/profile_sponsor',methods = ['GET','POST'])
@login_required
def profile_sponsor():
    if(current_user.id.startswith('spn')):
        if(request.method == 'GET'):
            image_sponsor = db.session.query(Images_Sponsor).filter_by(user_id = current_user.id).first()
            if(image_sponsor):
                return render_template('profile_sponsor.html',message = '',user = current_user,image_encoding = image_sponsor.image_encoding)
            else:
                return render_template('profile_sponsor.html',message = '',user = current_user)
        else:
            image = request.files['image']
            if(image):
                current_image = db.session.query(Images_Sponsor).filter_by(user_id = current_user.id).first()
                if(current_image):
                    db.session.delete(current_image)
                    image_data = image.read()
                    image_encoding = base64.b64encode(image_data).decode('utf-8')
                    new_image = Images_Sponsor(image_id = f'{ uuid.uuid4()}'[:7],image_name = f'{current_user.sponsor_name}_profile_img',image_encoding = image_encoding,user_id = current_user.id)
                    db.session.add(new_image)
                    current_user.sponsor_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    db.session.commit()
                    return render_template('profile_sponsor.html',image_encoding = image_encoding,user = current_user,message = 'changes saved successfully !')
                else:
                    image_data = image.read()
                    image_encoding = base64.b64encode(image_data).decode('utf-8')
                    new_image = Images_Sponsor(image_id = f'{ uuid.uuid4()}'[:7],image_name = f'{current_user.sponsor_name}_profile_img',image_encoding = image_encoding,user_id = current_user.id)
                    db.session.add(new_image)
                    current_user.sponsor_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    db.session.commit()
                    return render_template('profile_sponsor.html',image_encoding = image_encoding,user = current_user,message = 'changes saved successfully !')
            else:
                image_sponsor = db.session.query(Images_Sponsor).filter_by(user_id = current_user.id).first()
                if(image_sponsor):
                    current_user.sponsor_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    db.session.commit()
                    return render_template('profile_sponsor.html',image_encoding = image_sponsor.image_encoding,user = current_user,message = 'changes saved successfully !')
                else:
                    current_user.sponsor_name = request.form.get('name')
                    current_user.username = request.form.get('username')
                    current_user.email = request.form.get('email')
                    db.session.commit()
                    return render_template('profile_sponsor.html',user = current_user,message = 'changes saved successfully !')
    else:
        return render_template('unauthorized_access.html')



@app.route('/negotiation_requests',methods = ['GET'])
@login_required
def negotiation_requests():
    if(current_user.id.startswith('spn')):
        if(request.args.get('message') is None):
            negotiation_requests = db.session.query(Negotiation_Requests,Campaigns,Requests,Influencers).filter(Negotiation_Requests.sponsor_id == current_user.id,Negotiation_Requests.campaign_id == Campaigns.campaign_id,Negotiation_Requests.request_id == Requests.request_id,Negotiation_Requests.influencer_id == Influencers.id,Negotiation_Requests.status == 'Pending',Negotiation_Requests.flagged == False,Requests.campaign_id == Campaigns.campaign_id,Requests.flagged == False).all()
            return render_template('negotiation_requests.html',negotiation_requests = negotiation_requests,message = '')
        else:
            negotiation_requests = db.session.query(Negotiation_Requests,Campaigns,Requests,Influencers).filter(Negotiation_Requests.sponsor_id == current_user.id,Negotiation_Requests.campaign_id == Campaigns.campaign_id,Negotiation_Requests.request_id == Requests.request_id,Negotiation_Requests.influencer_id == Influencers.id,Negotiation_Requests.status == 'Pending',Negotiation_Requests.flagged == False,Requests.campaign_id == Campaigns.campaign_id,Requests.flagged == False).all()
            return render_template('negotiation_requests.html',negotiation_requests = negotiation_requests,message = request.args.get('message'))
    else:
        return render_template('unauthorized_access.html')



@app.route('/negotiation_accept',methods = ['GET'])
@login_required
def negotiation_accept():
    if(current_user.id.startswith('spn')):
        negotiation_request = db.session.query(Negotiation_Requests).filter(Negotiation_Requests.negotiation_id == request.args.get('negotiation_id'),Negotiation_Requests.flagged == False,Negotiation_Requests.status == 'Pending').first()
        if(negotiation_request):
            parent_campaign = db.session.query(Campaigns).filter_by(campaign_id = negotiation_request.campaign_id).first()
            requests = db.session.query(Requests).filter(Requests.campaign_id == parent_campaign.campaign_id,Requests.request_id != negotiation_request.request_id).all()
            payment_sum = 0
            for current_request in requests:
                    payment_sum += int(current_request.payment_amount)
            if(negotiation_request.desired_amount <= parent_campaign.budget - payment_sum):
                ad_request = db.session.query(Requests).filter_by(request_id = negotiation_request.request_id).first()
                ad_request.payment_amount = negotiation_request.desired_amount;ad_request.influencer_id = negotiation_request.influencer_id
                ad_request.status = 'Accepted';negotiation_request.status = 'Accepted'
                db.session.commit()
                return redirect(url_for('negotiation_requests',message = 'negotiation request accepted !'))
            else:
                negotiation_request.status = 'Rejected'
                db.session.commit()
                return redirect(url_for('negotiation_requests',message = 'desired amount exceeds campaign budget !'))
        else:
            return render_template('invalid_flagged.html',element = "Negotiation request")
    else:
        return render_template('unauthorized_access.html')   



@app.route('/negotiation_reject',methods = ['GET'])
@login_required
def negotiation_reject():
    if(current_user.id.startswith('spn')):
        negotiation_request = db.session.query(Negotiation_Requests).filter(Negotiation_Requests.negotiation_id == request.args.get('negotiation_id'),Negotiation_Requests.flagged == False,Negotiation_Requests.status == 'Pending').first()
        if(negotiation_request):
            negotiation_request.status = 'Rejected'
            db.session.commit()
            return redirect(url_for('negotiation_requests',message = 'negotiation request rejected !'))
        else:
            return render_template('invalid_flagged.html',element = "Negotiation request")
    else:
        return render_template('unauthorized_access.html')



def campaign_completion_check():
    with app.app_context():
        while(True):
            current_time = datetime.now()
            next_day = current_time.replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)
            seconds_until_next_day = (next_day - current_time).total_seconds()
            campaigns = db.session.query(Campaigns).filter_by(flagged = False).all()
            for campaign in campaigns:
                if(campaign.end_date <= current_time.date()):
                    campaign.status = 'Completed'
                    requests = db.session.query(Requests).filter_by(campaign_id = campaign.campaign_id,flagged = False).all()
                    for current_request in requests:
                        if(current_request.status == 'Accepted'):
                            current_request.status = 'Completed'
                        else:
                            current_request.status = 'N/A'
                        negotiation_requests = db.session.query(Negotiation_Requests).filter_by(request_id = current_request.request_id,flagged = False).all()
                        for negotiation_request in negotiation_requests:
                            if(negotiation_request.status == 'Pending'):
                                negotiation_request.status = 'N/A'
            db.session.commit()
            time.sleep(seconds_until_next_day)
        
        

@app.route('/campaign_status',methods = ['GET'])
@login_required
def get_data():
    if(current_user.id.startswith('spn')):
        campaigns = db.session.query(Campaigns).filter_by(sponsor_id = current_user.id,flagged = False).all()
        campaigns_list = []
        for campaign in campaigns:
            requests = db.session.query(Requests).filter_by(campaign_id = campaign.campaign_id,flagged = False).all()
            if(not requests):
                continue
            else:
                check = False
                for current_request in requests:
                    if(current_request.status == 'Accepted'):
                        check = True
                        break
                if(check):
                    campaigns_list.append(campaign.campaign_id)
        return campaigns_list
    else:
        return render_template('unauthorized_access.html')



@app.route('/add_campaign',methods = ['GET','POST'])
@login_required
def add_campaign():
    if(request.method == 'GET'):
        if(current_user.id.startswith('spn')):
            return render_template('add_campaign.html',message = '')
        else:
            return render_template('unauthorized_access.html')
    elif(request.method == 'POST'):
        if(current_user.id.startswith('spn')):
            data = request.form
            start_date = datetime.strptime(data['start_date'], r'%Y-%m-%d').date()
            if(start_date < date.today()):
                return render_template('add_campaign.html',message = 'start date must be \u2265 current date !')
            end_date = datetime.strptime(data['end_date'], r'%Y-%m-%d').date()
            if(start_date < end_date):
                if(data['visibility'] == 'Public'):
                    new_campaign = Campaigns(campaign_id = ('pbl'+f'{(uuid.uuid4())}')[:7],sponsor_id = current_user.id,campaign_name = data['campaign_name'],goal = data['campaign_goal'],campaign_field = current_user.industry,start_date = start_date,end_date = end_date,budget = data['budget'],visibility = data['visibility'])
                    db.session.add(new_campaign)
                    db.session.commit()
                    return render_template('add_campaign.html',message = 'campaign added successfully !')
                else:
                    new_campaign = Campaigns(campaign_id = ('pvt'+f'{(uuid.uuid4())}')[:7],sponsor_id = current_user.id,campaign_name = data['campaign_name'],goal = data['campaign_goal'],campaign_field = current_user.industry,start_date = start_date,end_date = end_date,budget = data['budget'],visibility = data['visibility'])
                    db.session.add(new_campaign)
                    db.session.commit()
                    return render_template('add_campaign.html',message = 'campaign added successfully !')
            else:
                return render_template('add_campaign.html',message = 'end date must be greater than start date !')
        else:
            return render_template('unauthorized_access.html')
        

     
@app.route('/delete_campaign',methods=['GET'])
@login_required
def delete_campaign():
    if(current_user.id.startswith('spn')):
        campaign_delete = db.session.query(Campaigns).filter(Campaigns.campaign_id == request.args.get('campaign_id'),Campaigns.flagged == False,Campaigns.status != 'Completed').first()
        if(campaign_delete):
            requests = db.session.query(Requests).filter_by(campaign_id = request.args.get('campaign_id')).all()
            for current_request in requests:
                if(current_request.status == 'Accepted'):
                    return redirect(url_for('dashboard_sponsor',message = 'campaign in progress !'))
            db.session.delete(campaign_delete)
            db.session.commit()
        else:
            return render_template('invalid_flagged.html',element = "Campaign") 
        return redirect(url_for('dashboard_sponsor',message = 'campaign deleted successfully !'))  
    else:
        return render_template('unauthorized_access.html')



@app.route('/edit_campaign',methods = ['GET'])
@login_required
def edit_campaign():
    if(current_user.id.startswith('spn')):
        if(sorted(list(request.args)) == ['campaign_id']):
            campaign = db.session.query(Campaigns).filter(Campaigns.campaign_id == request.args.get('campaign_id'),Campaigns.flagged == False,Campaigns.status != 'Completed').first()
            if(campaign):
                return render_template('edit_campaign.html',campaign = campaign,message = '')
            else:
                return render_template('invalid_flagged.html',element = "Campaign")
        elif(sorted(list(request.args)) == ['budget','campaign_id','end_date','start_date']):
            campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id'),flagged = False).first() 
            if(campaign):
                if(request.args.get('campaign_id') and request.args.get('start_date') and request.args.get('end_date')):
                    start_date = datetime.strptime(request.args.get('start_date'), r'%Y-%m-%d').date()
                    end_date = datetime.strptime(request.args.get('end_date'), r'%Y-%m-%d').date()
                    if(start_date < date.today()):
                        return render_template('edit_campaign.html',campaign = campaign,message = 'start date must be \u2265 current date !')
                    if(start_date < end_date):
                        campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first()
                        if(campaign.budget <= int(request.args.get('budget'))):
                            campaign.budget = request.args.get('budget')
                            campaign.start_date = datetime.strptime(request.args.get('start_date'), r'%Y-%m-%d').date()
                            campaign.end_date = datetime.strptime(request.args.get('end_date'), r'%Y-%m-%d').date()
                            db.session.commit()
                            return render_template('edit_campaign.html',campaign = campaign,message = 'changes saved successfully !')
                        else:
                            return render_template('edit_campaign.html',campaign = campaign,message = f'new budget must be \u2265 {campaign.budget} !')
                    else:
                        campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first()
                        return render_template('edit_campaign.html',campaign = campaign,message = 'end date must be greater than start date !')
                else:
                    campaign = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first()
                    return render_template('edit_campaign.html',campaign = campaign,message = 'input fields empty !')
            else:
                return render_template('invalid_flagged.html',element = "Campaign")
    else:
        return render_template('unauthorized_access.html')



@app.route('/campaign_requests',methods = ['GET'])
@login_required
def campaign_requests():
    if(current_user.id.startswith('spn')):
        if(request.args.get('message') is None):
            campaign = db.session.query(Campaigns).filter(Campaigns.campaign_id == request.args.get('campaign_id'),Campaigns.flagged == False,Campaigns.status != 'Completed').first()
            if(campaign):
                requests = db.session.query(Requests,Influencers).outerjoin(Influencers,Requests.influencer_id == Influencers.id).filter(Requests.campaign_id == request.args.get('campaign_id'),Requests.flagged == False).all()
                return render_template('campaign_requests.html',message = '',campaign = campaign,requests = requests)
            else:
                return render_template('invalid_flagged.html',element = "Campaign")
        else:
            campaign = db.session.query(Campaigns).filter(Campaigns.campaign_id == request.args.get('campaign_id'),Campaigns.flagged == False,Campaigns.status != 'Completed').first()
            if(campaign):
                requests = db.session.query(Requests,Influencers).outerjoin(Influencers,Requests.influencer_id == Influencers.id).filter(Requests.campaign_id == request.args.get('campaign_id'),Requests.flagged == False).all()
                return render_template('campaign_requests.html',message = request.args.get('message'),campaign = campaign,requests = requests)
            else:
                return render_template('invalid_flagged.html',element = "Campaign")
    else:
        return render_template('unauthorized_access.html')
    


@app.route('/add_request',methods = ['GET'])
@login_required
def add_request():
    if(current_user.id.startswith('spn')):
        campaign = db.session.query(Campaigns).filter(Campaigns.campaign_id == request.args.get('campaign_id'),Campaigns.flagged == False,Campaigns.status != 'Completed').first()
        if(campaign):
            if(sorted(list(request.args)) == ['campaign_id']):
                if(campaign.visibility == 'Public'):
                    return render_template('add_public_request.html',campaign_id =  campaign.campaign_id,message = '')
                elif(campaign.visibility == 'Private'):
                    return redirect(url_for('influencer_search',campaign_id = campaign.campaign_id))
            elif(sorted(list(request.args)) == ['campaign_id','influencer_id']):
                return render_template('add_pvt_request.html',campaign_id = request.args.get('campaign_id'),influencer_id = request.args.get('influencer_id'),message ='')
            elif(sorted(list(request.args)) == ['additional_notes','campaign_id','payment_amount','requirements']):
                if((request.args.get('requirements')) and (request.args.get('payment_amount')) and (request.args.get('additional_notes'))):
                    if(int(request.args.get('payment_amount')) < 10000):
                        return render_template('add_public_request.html',campaign_id = request.args.get('campaign_id'),message = 'payment amount must be greater than or equal to 10000 !')
                    campaign_budget = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first().budget
                    requests = db.session.query(Requests).filter_by(campaign_id = request.args.get('campaign_id')).all()
                    payment_sum = 0
                    for current_request in requests:
                            payment_sum += int(current_request.payment_amount)
                    if(int(request.args.get('payment_amount')) <= campaign_budget - payment_sum):
                        new_public_request = Requests(request_id = f'{(uuid.uuid4())}'[:7],sponsor_id = current_user.id,campaign_id = request.args.get('campaign_id'),payment_amount = request.args.get('payment_amount'),additional_notes = request.args.get('additional_notes'),
                        requirements = request.args.get('requirements'))
                        db.session.add(new_public_request)
                        db.session.commit()
                        return render_template('add_public_request.html',campaign_id = request.args.get('campaign_id'),message = 'request created successfully !')
                    else:
                        return render_template('add_public_request.html',campaign_id = request.args.get('campaign_id'),message = 'payment amount exceeds campaign budget !')
                else:
                    return render_template('add_public_request.html',campaign_id = request.args.get('campaign_id'),message = 'input fields empty !')
            elif(sorted(list(request.args)) == ['additional_notes','campaign_id','influencer_id','payment_amount','requirements']):
                if((request.args.get('requirements')) and (request.args.get('payment_amount')) and (request.args.get('additional_notes'))):
                    if(int(request.args.get('payment_amount')) < 10000):
                        return render_template('add_pvt_request.html',campaign_id = request.args.get('campaign_id'),influencer_id = request.args.get('influencer_id'),message = 'payment amount must be greater than or equal to 10000 !')
                    campaign_budget = db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first().budget
                    requests = db.session.query(Requests).filter_by(campaign_id = request.args.get('campaign_id')).all()
                    payment_sum = 0
                    for current_request in requests:
                        if(current_request.status != 'Rejected'):
                            payment_sum += int(current_request.payment_amount)
                    if(int(request.args.get('payment_amount')) <= campaign_budget - payment_sum):
                        new_pvt_request = Requests(request_id = f'{(uuid.uuid4())}'[:7],sponsor_id = current_user.id,influencer_id = request.args.get('influencer_id'),campaign_id = request.args.get('campaign_id'),payment_amount = request.args.get('payment_amount'),additional_notes = request.args.get('additional_notes'),requirements = request.args.get('requirements'))
                        db.session.add(new_pvt_request)
                        db.session.commit()
                        return render_template('add_pvt_request.html',campaign_id = request.args.get('campaign_id'),influencer_id = request.args.get('influencer_id'),message = 'request created successfully !')
                    else:
                        return render_template('add_pvt_request.html',campaign_id = request.args.get('campaign_id'),influencer_id = request.args.get('influencer_id'),message = 'payment amount exceeds campaign budget !')
                else:
                    return render_template('add_pvt_request.html',campaign_id = request.args.get('campaign_id'),influencer_id = request.args.get('influencer_id'),message = 'input fields empty !')
        else:
            return render_template('invalid_flagged.html',element = "Campaign")
    else:
        return render_template('unauthorized_access.html')



@app.route('/edit_request', methods=['GET'])
@login_required
def edit_request():
    if(current_user.id.startswith('spn')):
        if(sorted(list(request.args)) == ['request_id']):
            current_request = db.session.query(Requests).filter(Requests.request_id == request.args.get('request_id'),Requests.flagged == False,Requests.status != 'Completed').first()
            if(current_request):
                return render_template('edit_request.html',request_id = request.args.get('request_id'),current_request = current_request,message = '')
            else:
                return render_template('invalid_flagged.html',element = "Request")
        elif(sorted(list(request.args)) == ['additional_notes','campaign_id','influencer_id','payment_amount','request_id','requirements']):
            current_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id'),flagged = False).first()
            if(current_request):
                if((request.args.get('requirements')) and (request.args.get('payment_amount')) and (request.args.get('additional_notes'))):
                    if(int(request.args.get('payment_amount')) < 10000):
                        return render_template('edit_request.html',current_request = current_request,message = 'payment amount must be greater than or equal to 10000 !')
                    campaign_budget = int(db.session.query(Campaigns).filter_by(campaign_id = request.args.get('campaign_id')).first().budget)
                    requests = db.session.query(Requests).filter(Requests.campaign_id == request.args.get('campaign_id'),Requests.request_id != request.args.get('request_id')).all()
                    payment_sum = 0
                    for current_request in requests:
                        payment_sum += int(current_request.payment_amount)
                    if(int(request.args.get('payment_amount')) <= campaign_budget - payment_sum):
                        edit_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first()
                        edit_request.requirements = request.args.get('requirements')
                        edit_request.payment_amount = request.args.get('payment_amount')
                        edit_request.additional_notes = request.args.get('additional_notes')
                        db.session.commit()
                        current_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first()
                        return render_template('edit_request.html',current_request = current_request,message = 'changes saved successfully !')
                    else:
                        current_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first()
                        return render_template('edit_request.html',current_request = current_request,message = 'payment amount exceeds campaign budget !')
                else:
                    current_request = db.session.query(Requests).filter_by(request_id = request.args.get('request_id')).first()
                    return render_template('edit_request.html',current_request = current_request,message = 'input fields empty !')
            else:
                return render_template('invalid_flagged.html',element = "Request") 
    else:
        return render_template('unauthorized_access.html')



@app.route('/delete_request',methods=['GET'])
@login_required
def delete_request():
    if(current_user.id.startswith('spn')):
        request_delete = db.session.query(Requests).filter(Requests.request_id == request.args.get('request_id'),Requests.flagged == False,Requests.status != 'Completed').first()
        if(request_delete):
            campaign_id = request_delete.campaign_id
            db.session.delete(request_delete)
            db.session.commit()
            return redirect(url_for('campaign_requests',campaign_id = campaign_id,message = 'request deleted successfully !'))
        else:
            return render_template('invalid_flagged.html',element = "Request") 
    else:
        return render_template('unauthorized_access.html')
    


@app.route('/influencer_search',methods = ['GET','POST'])
@login_required
def influencer_search():
    if(current_user.id.startswith('spn')):
        if(request.method == 'GET' and sorted(list(request.args)) == ['campaign_id']):
            return render_template('influencer_search.html',campaign_id = request.args.get('campaign_id'))
        elif(request.method == 'GET' and sorted(list(request.args)) == ['campaign_id','followers','niche']):
            influencers = db.session.query(Influencers).filter_by(niche = request.args.get('niche'),followers = request.args.get('followers'),flagged = False).all()
            return render_template('influencer_search.html',campaign_id = request.args.get('campaign_id'),influencers = influencers)
        
#--------------------------------------#

@app.route('/logout',methods = ['GET'])
@login_required
def logout():
    current_user.is_authenticated = False
    db.session.commit() 
    logout_user()
    return redirect(url_for('home',message = 'logged out successfully !'))

#--------------------------------------#

if(__name__ == '__main__'):
    with app.app_context():
        db.create_all()
        date_thread = threading.Thread(target=campaign_completion_check, daemon=True)
        date_thread.start()
    app.run(debug=True)