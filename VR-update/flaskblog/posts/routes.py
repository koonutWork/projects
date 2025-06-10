# Importing required Libraries
from flask import (render_template, url_for, flash,redirect, request, abort, Blueprint, session,jsonify)
from flask import current_app
from flaskblog.models import Library, Experience, Question_option, Conversation, Video, Feedback, Avatar, Dragged_video, Hotspot,Node,Virtuals
from flaskblog.posts.forms import PostForm, ExperienceForm
from flaskblog import db
from flaskblog.users.utils import save_video
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func
import shutil
import time
import os

# Registering post
posts = Blueprint('posts', __name__)

# -------  Function to get images from the Library folders ----------------------------------------
def get_images(directory):
    image_files = []
    for file in os.listdir(directory):
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_files.append(file)
            print(image_files)
    return image_files


# --------- Function to get videos from the Library folders  ----------------------------------------
def get_videos(directory):
    video_files = []
    for file in os.listdir(directory):
        if file.endswith(('mp4', 'avi', 'mov', 'mkv', 'wmv')):
            video_files.append(file)
            print(video_files)
    return video_files


# ---------- Restriction and allowing particular format for Image uploads and save -------------------
def allowed_file_img(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- Restriction and allowing particular format for video uploads and save -------------------
def allowed_video(filename):
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ----------- Route for the new library to create libary and update the database ----------------------
# ----------- This page is for Create library ---------------------------------------------------------
@posts.route("/Library/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Library(title=form.title.data,
                           content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            sanitized_title = secure_filename(post.title)
            flash('Your Library has been created!', 'success')  # Notification for Library created after saving to database
            
            # Construct the full path to the target directory
            target_path = os.path.join(
                current_app.root_path, 'static', "Library")
            
            # Create the directory folder with the Library name
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            target_path = os.path.join(
                current_app.root_path, 'static', "Library", sanitized_title)
            os.mkdir(target_path)
        except FileExistsError:
            print("Folder 'for_CHECK' already exists.")
        return redirect(url_for('main.home'))
    # Renders the create library page
    return render_template('create_Library.html', title='New Library', form=form, legend='Create a New Library')

# ----------- Route for the Existing library to view libaries ----------------------------------------------
# ----------- This page Updates library, Creates Experiences and deletes the current library ---------------
@posts.route("/Library/existing", methods=['GET', 'POST'])
@login_required
def existing_experience():
    page = request.args.get('page', 1, type=int)
    posts = Library.query.order_by(
        Library.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('existing_libraries.html', posts=posts, legend='Existing Libraries')

# ----------- Route for the Existing library to modify libaries and link for Create Experience -------------
# ----------- This page Updates library, Creates Experiences and deletes the current library ---------------
@posts.route("/Library/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Library.query.get_or_404(post_id)
    current_post = Experience.query.filter(Experience.post_id == post_id)
    expId = request.form.get('eid', type=int)
    if (expId != None):
        dele = Experience.query.filter(Experience.eid == expId).first()
        conversations = Conversation.query.filter(
            Conversation.experience_id == expId).all()
        for conversation in conversations:
            db.session.delete(conversation)
        db.session.delete(dele)
        db.session.commit()
    return render_template('Library.html', title=post.title, post=post, experiences=current_post)

# ----------- Route for the Existing library to Update current libaries --------------------------------------
# ----------- This page Updates the current library ----------------------------------------------------------
@posts.route("/Library/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Library.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Library has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_Library.html', title='Update Post',
                           form=form, legend='Update Post')

# ----------- Route for the Delete of Existing library ------------------------------------------------------
# ----------- This page Deletes the current library and returns to home page --------------------------------
@posts.route("/Library/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Library.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # Delete related experiences and conversations
    experiences = Experience.query.filter_by(post_id=post_id).all()
    for experience in experiences:
        # Delete related conversations
        conversations = Conversation.query.filter_by(
            experience_id=experience.eid).all()
        for conversation in conversations:
            db.session.delete(conversation)

        db.session.delete(experience)

    db.session.delete(post)
    db.session.commit()
    flash('Your Library has been deleted!', 'success')
    return redirect(url_for('main.home'))

# ----------- Route for Creating new experience based on the Library ID ------------------------------------------------------
# ----------- This page gives option for creating diffrent Experiences -------------------------------------------------------

@posts.route("/experience/new/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_experience(post_id):
    form = ExperienceForm()
    if form.validate_on_submit():
        experience = Experience(
            etitle=form.etitle.data, econtent=form.econtent.data, user_id=current_user.id, post_id=post_id)
        db.session.add(experience)
        db.session.commit()
        flash('Your experience has been created!', 'success')
        return redirect(url_for('main.home'))
    elif form.virtual_tour.data:
        text_type = "Virtualtour"
        experience = Experience(etitle=form.etitle.data, econtent=form.econtent.data,
                                user_id=current_user.id, post_id=post_id, ex_type=text_type)
        db.session.add(experience)
        db.session.commit()
        return redirect(url_for('posts.virtualtour'))
    elif form.switching_perspective.data:
        text_type = "Switching"
        experience = Experience(etitle=form.etitle.data, econtent=form.econtent.data,
                                user_id=current_user.id, post_id=post_id, ex_type=text_type)
        db.session.add(experience)
        db.session.commit()
        return redirect(url_for('posts.switching'))
    elif form.conversation.data:
        text_type = "Conversation"
        library_instance = Library.query.get(post_id)
        experience_instance = Experience(etitle=form.etitle.data, econtent=form.econtent.data,
                                         user_id=current_user.id, post_id=post_id, ex_type=text_type)
        db.session.add(experience_instance)
        db.session.commit()
        late_ex = db.session.query(func.max(Experience.eid)).scalar()
        current_library = db.session.query(Experience.post_id).filter(
            Experience.eid == late_ex).scalar()
        conversation = Conversation(
            library_id=current_library, experience_id=late_ex)
        db.session.add(conversation)
        db.session.commit()
        late_con = db.session.query(func.max(Conversation.id)).scalar()
        con = Experience.query.filter_by(eid=late_ex, post_id=current_library)
        return redirect(url_for('posts.conversation', con=con, late_con=late_con, questions=None, optionCount=0, optionCountO=0, new=1))
    return render_template('create_experience.html', title='New Experience', form=form, legend='New Experience')

#  -------------------------------------------------------------------------------------------------------------------------------------------------  #



# ----------- Route for Creating new experience based on the Library ID ------------------------------------------------------
# ----------- This page gives option for creating diffrent Experiences -------------------------------------------------------

@posts.route('/virtualtour', methods=['GET', 'POST'])
@login_required
def virtualtour():
    
    
    
    optionCount = request.args.get('optionCount', type=int)
    optionCountO = request.args.get('optionCountO', type=int)
    buttonCount = request.args.get('button_count', type=int)
    late_ex = db.session.query(func.max(Experience.eid)).scalar()

    try:
        text_type="Virtualtour"
        late_ex = db.session.query(func.max(Experience.eid)).filter(Experience.ex_type == text_type).scalar()
        current_library = db.session.query(Experience.post_id).filter(
            Experience.eid == late_ex).scalar()
        con = Experience.query.filter_by(
            eid=late_ex, post_id=current_library).first()
        lib = Library.query.filter_by(id=current_library).first()
        library_title = secure_filename(lib.title)
        experience_title = secure_filename(con.etitle)
        library_folder_name = secure_filename(lib.title)
        experience_folder_name = secure_filename(con.etitle)
        session['library_folder_name'] = library_folder_name
        session['experience_folder_name'] = experience_folder_name
        video_folder_path = os.path.join(
        current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
        
        # ---------------  Video upload and save functions ------------------------------------------
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'files[]' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            files = request.files.getlist('files[]')
            uploaded_files = []
            for file in files:
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    # flash('No selected file')
                    return redirect(request.url)
                if file and allowed_video(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(video_folder_path, filename))
                    uploaded_files.append(filename)
            # flash('Files uploaded successfully')
            # Join the filenames into a comma-separated string
            filenames_string = ','.join(uploaded_files)
            text_type = "Virtualstour"
            buttonCount = request.args.get('button_count', type=int)
            late_ex = db.session.query(func.max(Experience.eid)).scalar()
            current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
            conversation = Conversation(library_id=current_library, experience_id=late_ex)
            db.session.add(conversation)
            db.session.commit()
            
            library_title = secure_filename(lib.title)
            experience_title = secure_filename(con.etitle)
        
        # Construct the full path to the target directory
        target_path = os.path.join(
                current_app.root_path, 'static', "Library", library_title, experience_title)
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_video")
            # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_video")
            # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_images")
            # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_images")
            # Create the directory
        os.mkdir(target_path)
    except FileExistsError:
        print("Folder 'for_CHECK' already exists.")
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    
    hotsp=db.session.query(Hotspot).filter(Hotspot.ex_id == late_ex).all()
    return render_template('virtualtour.html', title='virtual_tour_Page', con=con, lib=lib, buttonCount=buttonCount,library_folder_name=library_folder_name, experience_folder_name=experience_folder_name,video_files=video_files,hotsp=hotsp)

# -------------------------------------------------
# creating a post for virtual tour hotspot page
def get_next_node_name():
    node_count=db.session.query(func.max(Node.id)).scalar()
    node_name = f"Node {node_count}"
    node_count += 1
    return node_name

@posts.route('/hotspot', methods=['GET', 'POST'])
@login_required
def hotspot():
    
    # Session related
    filename_vv = session.get('filename_vv', None)
    
    exp_id= request.form.get('exp_id',type=int)
    text_type="Virtualtour"
    late_ex = db.session.query(func.max(Experience.eid)).filter(Experience.ex_type == text_type).scalar()
    current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    name_hot = request.form.get('name_hot')
    hotspot_count = db.session.query(Hotspot).filter(Hotspot.ex_id == exp_id).count()
    vt = Virtuals(root='root',ex_id=late_ex,video=filename_vv)
    db.session.add(vt)
    db.session.commit()
    get_v_id=Virtuals.query.filter_by(id=late_ex).first()
    
    print("exp_id :", exp_id)
    
    name_hot = request.form.get('name_hot')
    print("NAME", name_hot)
    if name_hot != None:
            xcor=request.form.get('x_value')
            ycor=request.form.get('y_value')
            time_hot = request.form.get('currentTime')
            scrub = request.form.get('scrub1', type=int)
            main_p = request.form.get('main_p', type=int)
            video=request.form.get('selectedVideoPath')
            exp_id= request.form.get('exp_id', type=int)
            existing_hotspot = db.session.query(Hotspot).filter(Hotspot.name == name_hot).filter(Hotspot.ex_id == exp_id).first()
            print("x:",xcor)
            if not existing_hotspot:
                
                get_v_id=Virtuals.query.filter_by(id=late_ex).first()
               
                new_hotspot = Hotspot(name=name_hot, time=time_hot, scrub=scrub, main_p=main_p, video=video, x_cor=xcor, y_cor=ycor,ex_id=exp_id,v_id=get_v_id.id)
                db.session.add(new_hotspot)
                db.session.commit()
                data = {
                    'nodes': [
                                {'name': get_next_node_name(), 'parent_id': '3'}
                            ]
                        }
                # Create a request context for update_tree
                with current_app.test_request_context('/update_tree', method='POST', json=data):
                 # Call update_tree directly
                    update_tree_response = update_tree()
                    print(update_tree_response.get_data(as_text=True))
                    flash('New Hotspot added successfully!', 'success')
                    all_hotspot=db.session.query(Hotspot).filter(Hotspot.ex_id == exp_id).filter(Hotspot.v_id == get_v_id.id).all()
                return render_template("hotspot.html", post=post, con=con, lib=lib,filename_vv=filename_vv,all_hotspot=all_hotspot)
            else:
                flash('This Hotspot name already exists!', 'danger')
    all_hotspot=db.session.query(Hotspot).filter(Hotspot.ex_id == exp_id).all()
    
    return render_template("hotspot.html", post=post, con=con, lib=lib,filename_vv=filename_vv,all_hotspot=all_hotspot)
# -------------------------------------------------
# creating a post for hotspot settings page

@posts.route('/hotspotsettings', methods=['GET'])
@login_required
def hotspotsettings():
    return render_template("hotspotsettings.html", post=post)






n=1
op=1
# -------------------------------------------------
# creating a post for conversation page
@posts.route('/conversation', methods=['GET', 'POST'])
@login_required
def conversation():
    new = request.args.get('new')
    print('new :', new)
    if new == 1:
        questions = ''
        db.session.add(conversation)
        db.session.commit()
        return render_template('conrversation.html', title='Conversation Page',
                               optionCount=0, optionCountO=0, con=con, lib=lib, current_show=current_show,type_current=type_current, question='None')
    elif new == None:
        questions = request.form.get('question')
        options_list = request.form.getlist('options[]')
        scores = request.form.getlist('scores[]')
        optionCount = request.form.get('optionCount', type=int)
        optionCountO = request.form.get('optionCountO', type=int)

        # store the data
        
        
        optionCountO = request.form.get('optionCountO', type=int)
        print("count: ", optionCount)
        print("countO: ", optionCountO)
        print("data :", questions, scores, options_list, optionCount)
        text_type="Conversation"
        late_ex = db.session.query(func.max(Experience.eid)).filter(Experience.ex_type == text_type).scalar()
        current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
        conversation = Conversation(library_id=current_library, experience_id=late_ex)
        con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
        lib = Library.query.filter_by(id=current_library).first()
        type_current = Conversation.query.filter_by(library_id=current_library, experience_id=late_ex).first()

        # get data from form in array
        s_name = request.form.getlist('name[]')
        score1 = request.form.getlist('score1[]')
        score2 = request.form.getlist('score2[]')
        score3 = request.form.getlist('score3[]')
        print("data:", s_name, score1, score2, score3)
        for i in range(0, len(s_name)):
            
            feedback = Feedback(
                score_name=s_name[i], point1=score1[i], point2=score2[i], point3=score3[i])
            db.session.add(feedback)
            db.session.commit()
            late_q = db.session.query(func.max(Question_option.question_id)).scalar()
            current_show = Question_option.query.filter_by(question_id = late_q)
            return render_template('conversation.html', title='Conversation Page',optionCount=optionCount, current_show=current_show,optionCountO=optionCountO, con=con, lib=lib, type_current=type_current)
        print("question :", questions)
        if questions == 'None':  
            db.session.add(conversation)
            
            return render_template('conversation.html', title='Conversation Page',optionCount=optionCount, current_show=current_show,optionCountO=optionCountO, con=con, lib=lib, type_current=type_current)
        else:
            db.session.add(conversation)
            db.session.commit()
            session['n']=1
            session['op']=1
            optionCount=1
            I_i=0
            n = session.get('n',1)  # Default to 1 if not set
            op = session.get('op',1)
            for i in range(0, optionCount):
                #if: question is added to the database to be root
                con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
                this_question = Question_option(question_id=n, question_txt=questions, option_id=i+op, option_txt=options_list[i], option_score=scores[i], parent_question=None, conversation_id=con.eid)
                I_i+=1
                db.session.add(this_question)
                db.session.commit()
            session['n'] += 1
            session['op'] += I_i
            print("Q_id:",n)
            late_q = db.session.query(func.max(Question_option.question_id)).scalar()
            current_show = Question_option.query.filter_by(question_id = late_q)
            print(current_show)
            if optionCount is not None:
                optionCount = int(optionCount)
            else:
                optionCount = 0

            library_folder_name = secure_filename(lib.title)
            experience_folder_name = secure_filename(con.etitle)
            video_folder_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
            video_files = get_videos(video_folder_path)
            return render_template('conversation.html', title='Conversation Page',
                                   optionCount=optionCount, optionCountO=optionCountO,current_show=current_show, con=con, lib=lib, type_current=type_current, question=questions,library_folder_name=library_folder_name, experience_folder_name=experience_folder_name,video_files=video_files)
        
    try:
        
        late_ex = db.session.query(func.max(Experience.eid)).scalar()
        current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
        lib = Library.query.filter_by(id=current_library).first()
        con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
        type_current = Conversation.query.filter_by(library_id=current_library, experience_id=late_ex).first()
        library_title = secure_filename(lib.title)
        experience_title = secure_filename(con.etitle)
        library_title = secure_filename(lib.title)
        experience_title = secure_filename(con.etitle)
        library_folder_name = secure_filename(lib.title)
        experience_folder_name = secure_filename(con.etitle)
        session['library_folder_name'] = library_folder_name
        session['experience_folder_name'] = experience_folder_name
        video_folder_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
        # ---------------  Video upload and save functions ------------------------------------------
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'files[]' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            files = request.files.getlist('files[]')
            uploaded_files = []
            for file in files:
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    # flash('No selected file')
                    return redirect(request.url)
                if file and allowed_video(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(video_folder_path, filename))
                    uploaded_files.append(filename)
            # flash('Files uploaded successfully')
        # Construct the full path to the target directory

        target_path = os.path.join(
            current_app.root_path, 'static', "Library", library_title, experience_title)
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_video")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_video")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_images")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_images")
        # Create the directory
        os.mkdir(target_path)
    except FileExistsError:
        print("Folder 'for_CHECK' already exists.")
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    current_show = Question_option.query.filter_by(question_id = 1)
    return render_template('conversation.html', title='Conversation Page',
                           optionCount=0, optionCountO=0, con=con, lib=lib, type_current=type_current,current_show=current_show, question='None',library_folder_name=library_folder_name, experience_folder_name=experience_folder_name,video_files=video_files)
# -------------------------------------------------
# creating a post for options page


@posts.route('/options', methods=['GET', 'POST'], endpoint='options')
@login_required
def options():
    return render_template("options.html", post=post)


@posts.route('/conversation_edit', methods=['GET', 'POST'])
@login_required
def conversation_edit():
    return render_template("conversation_edit.html", post=post)

# ------------------------------------------------------
# creating a post for 3rd row display


@posts.route('/options_options', methods=['GET', 'POST'])
@login_required
def options_options():
    # post = Post.query.get_or_404(post_id)
    return render_template("options_options.html", post=post)


@posts.route('/media_Library')
@login_required
def media_Library():
    # post = Post.query.get_or_404(post_id)
    return render_template("media_Library.html", post=post, title='Media Library Page')

# -------------------------------------------------
# creating a Feedback for conversation page


@posts.route('/Feedbackcon', methods=['GET', 'POST'])
@login_required
def Feedbackcon():
    # post = Post.query.get_or_404(post_id)
    return render_template("Feedbackcon.html", post=post)







# -----------------------------------------------------
# -------------------------------------------------
# creating a post for conversation page


@posts.route('/conversationlist')
@login_required
def conversationlist():

    current_library = request.args.get('library_id', type=int)
    late_ex = request.args.get('experience_id', type=int)
    optionCount = request.args.get('optionCount', type=int)
    optionCountO = request.args.get('optionCountO', type=int)
    con = Experience.query.filter_by(
        eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    type_current = Conversation.query.filter_by(
        library_id=current_library, experience_id=late_ex).first()
    # type_current=Conversation.query.filter_by(id=current_con)
    current_show = Question_option.query.filter_by(question_id = 1)
    current_question = Question_option.query.filter_by(question_id = 1).first()
    if current_question != None:
        question=current_question.question_txt
        return render_template('conversation.html', title='Conversation Page', optionCount=optionCount, optionCountO=optionCountO, con=con, lib=lib, current_show=current_show,question=question)
    return render_template('conversation.html', title='Conversation Page', optionCount=optionCount, optionCountO=optionCountO, con=con, lib=lib, current_show=current_show)


# -------------------------------------------------------------
# creating a post for Switching perspective page
@posts.route('/Switching', methods=['GET', 'POST'])
@login_required
def switching():
    #----------------------------------------------------------------
    #getting data from avatar_option page
    name = request.form.get('name')
    description = request.form.get('description')
    scrub = request.form.get('scrub', type=int)
    main_p = request.form.get('main_p', type=int)
    video_files= request.form.get('video_files')
    image_files=request.form.get('avatar_image')
   
    exid_now=session.get('ex_id', None)

    if scrub==None:
        scrub=0
    if main_p==None:
        main_p=0
    # if name not empty then insert data
    if name != None:
        ava = Avatar(avatar_name=name, description=description,scrub=scrub, main_p=main_p,video=video_files,img=image_files,ex_id=exid_now)
        db.session.add(ava)
        db.session.commit()
    
    try:       
        text_type = "Switching"
        
        late_ex = db.session.query(func.max(Experience.eid)).filter(Experience.ex_type == text_type).scalar()
        current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
        con = Experience.query.filter_by(
            eid=late_ex, post_id=current_library).first()
        session['ex_id'] = con.eid
        lib = Library.query.filter_by(id=current_library).first()
        library_title = secure_filename(lib.title)
        experience_title = secure_filename(con.etitle)
        library_folder_name = secure_filename(lib.title)
        experience_folder_name = secure_filename(con.etitle)
        session['library_folder_name'] = library_folder_name
        session['experience_folder_name'] = experience_folder_name
        exid_now=session.get('ex_id', None)
        #---for show all the avater that belong to this experiment of switching
        avatar_all = db.session.query(Avatar).filter(Avatar.ex_id==late_ex).all()
        avatar_all_serializable = []
        #------loop data
        for avatar in avatar_all:
            avatar_dict = {
                'id': avatar.id,
                'avatar_name': avatar.avatar_name,
                'description': avatar.description,
                'scrub': avatar.scrub,
                'main_p': avatar.main_p,
                'video': avatar.video,
                'img': avatar.img
                # Add more fields if necessary
            }
            avatar_all_serializable.append(avatar_dict)
 
        avatar_all_length = len(avatar_all_serializable)
        
        avatar_max=db.session.query(func.max(Avatar.id)).scalar()
        
        

        # path for the temp image and video
        image_folder_path = os.path.join(
            current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_images")
        # print(image_folder_path)
        video_folder_path = os.path.join(
            current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
        # print(video_folder_path)
        # path for the seleced image
        image_folder_selected = os.path.join(
            current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "selected_images")
        # print(image_folder_selected)
        
        
        # ---------------  Image selected upload and save functions ------------------------------------------
        if request.method == 'POST':
            # Check if the post request has the file part
            if 'files[]' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            # Determine the target folder based on the flag
            target_folder_flag = request.form.get('target_folder', 'default')  # 'default' is a fallback value
            if target_folder_flag == 'selected':
                target_folder = image_folder_selected
            else:
                target_folder = image_folder_path
            files = request.files.getlist('files[]')
            uploaded_files = []
            for file in files:
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    # flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file_img(file.filename):
                    filename = secure_filename(file.filename)
                    current_app.logger.info(filename)
                    print(filename)
                    # After saving selected image files
                    file.save(os.path.join(target_folder, filename))
                    uploaded_files.append(filename)
            # flash('Files uploaded successfully')
            # Join the filenames into a comma-separated string
            filenames_string = ','.join(uploaded_files)

        if request.method == 'POST':
            # Check if the post request has the file part
            if 'files[]' not in request.files:
                # flash('No file part')
                return redirect(request.url)
            files = request.files.getlist('files[]')
            uploaded_files = []
            for file in files:
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    # flash('No selected file')
                    return redirect(request.url)
                if file and allowed_video(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(video_folder_path, filename))
                    uploaded_files.append(filename)
            # flash('Files uploaded successfully')
            # Join the filenames into a comma-separated string
            filenames_string = ','.join(uploaded_files)
    
    # You can now use video_folder_path as needed in this function
    # For demonstration, let's just print it

    # Construct the full path to the target directory
        target_path = os.path.join(
            current_app.root_path, 'static', "Library", library_title, experience_title)
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_video")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_video")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "temp_images")
        # Create the directory
        os.mkdir(target_path)
        target_path = os.path.join(current_app.root_path, 'static',
                                   "Library", library_title, experience_title, "selected_images")
        # Create the directory
        os.mkdir(target_path)
    except FileExistsError:
        print("Folder 'for_CHECK' already exists.")
    image_files = get_images(image_folder_path)
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    
    current_show = Question_option.query.filter_by(question_id = 1)
    return render_template('Switching.html', title='Conversation Page', con=con, lib=lib, image_files=image_files, video_files=video_files, image_folder_path=image_folder_path, library_folder_name=library_folder_name, experience_folder_name=experience_folder_name, avatar_all=avatar_all_serializable, avatar_all_length=avatar_all_length)




@posts.route('/avatar_option', methods=['GET', 'POST'])
@login_required
def avatar_option():
    
    # Retrieve video_folder_path from session
    library_folder_name = session.get('library_folder_name', None)
    experience_folder_name = session.get('experience_folder_name', None)
    video_files = session.get('video_files', None)
    
    # Assuming fileName_sel starts as None
    fileName_sel = None
    # Later in your code, when receiving fileName_sel values
    received_value = request.form.get('fileName_sel')
    exid=request.form.get('eid',type=int)
    if exid is not None:
        ex_id = exid
        # Now you can use ex_id knowing it's not None if a value was received
        print("EID :",exid)
        session['ex_id'] = ex_id
    # Check if received_value is not None, then update ex_id
    if received_value is not None:
        fileName_sel = received_value
        # Now you can use fileName_sel knowing it's not None if a value was received
        print("filename:", fileName_sel)
        session['Selected_image_avatar'] = fileName_sel

    
    video_folder_path = os.path.join(current_app.root_path, 'static', "Library",
                                     library_folder_name, experience_folder_name, "selected_video")
    image_folder_path = os.path.join(current_app.root_path, 'static', "Library",
                                     library_folder_name, experience_folder_name, "selected_image")
    # print(video_folder_path)
    # ---------------  Video upload and save functions ------------------------------------------
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and allowed_video(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(video_folder_path, filename))
                uploaded_files.append(filename)
        # flash('Files uploaded successfully')
        # Join the filenames into a comma-separated string
        filenames_string = ','.join(uploaded_files)
    
    # print(image_files_avatar)
    # You can now use video_folder_path as needed in this function
    # For demonstration, let's just print it
    # print(experience_folder_name)
    # print(video_files)
    # post = Post.query.get_or_404(post_id)
    avatar_image_name = session.get('Selected_image_avatar', None)
    print(avatar_image_name)
    ex_id_now=session.get('ex_id', None)
    return render_template("avatar_option.html", post=post, ex_id=ex_id_now,library_folder_name=library_folder_name, experience_folder_name=experience_folder_name, video_files=video_files, avatar_image_name=avatar_image_name)

@posts.route('/switchinglist', methods=['GET', 'POST'])
@login_required
def switchinglist():
    current_library = request.args.get('library_id', type=int)
    late_ex = request.args.get('experience_id', type=int)
    #get only avatar that belong to this ex_id
    avatar_all = db.session.query(Avatar).filter(Avatar.ex_id==late_ex).all()
    avatar_all_serializable = []
#get detail of the avatar
    for avatar in avatar_all:
            avatar_dict = {
                'id': avatar.id,
                'avatar_name': avatar.avatar_name,
                'description': avatar.description,
                'scrub': avatar.scrub,
                'main_p': avatar.main_p,
                'video': avatar.video,
                'img': avatar.img
                # Add more fields if necessary
            }
            avatar_all_serializable.append(avatar_dict)

    name = request.form.get('name')
    description = request.form.get('description')
    scrub = request.form.get('scrub', type=int)
    main_p = request.form.get('main_p', type=int)
    print("scrub :", scrub)
    if name != None:
        ava = Avatar(avatar_name=name, description=description,
                     scrub=scrub, main_p=main_p)
        db.session.add(ava)
        db.session.commit()
    
    con = Experience.query.filter_by(
        eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    type_current = Conversation.query.filter_by(
        library_id=current_library, experience_id=late_ex).first()
    library_folder_name = secure_filename(lib.title)
    experience_folder_name = secure_filename(con.etitle)
    session['library_folder_name'] = library_folder_name
    session['experience_folder_name'] = experience_folder_name
    # type_current=Conversation.query.filter_by(id=current_con)

    # path for the image and video
    image_folder_path = os.path.join(
        current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_images")
    print(image_folder_path)
    video_folder_path = os.path.join(
        current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
    print(video_folder_path)
    # Store video_folder_path in session
    # path for the image and video selected
    image_folder_selected = os.path.join(
        current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "selected_images")
    print(image_folder_selected)

    # ---------------  Image selected upload and save functions ------------------------------------------
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        # Determine the target folder based on the flag
        target_folder_flag = request.form.get('target_folder', 'default')  # 'default' is a fallback value
        if target_folder_flag == 'selected':
            target_folder = image_folder_selected
        else:
            target_folder = image_folder_path
        files = request.files.getlist('files[]')
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and allowed_file_img(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(target_folder, filename))
                uploaded_files.append(filename)
        # flash('Files uploaded successfully')
        # Join the filenames into a comma-separated string
        filenames_string = ','.join(uploaded_files)

    # ---------------  Video upload and save functions ------------------------------------------
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and allowed_video(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(video_folder_path, filename))
                uploaded_files.append(filename)
        # flash('Files uploaded successfully')
        # Join the filenames into a comma-separated string
        filenames_string = ','.join(uploaded_files)
    #get the image_file and video_files from the session
    image_files = get_images(image_folder_path)
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    current_show = Question_option.query.filter_by(question_id = 1)
    return render_template('Switching.html', title='Conversation Page',avatar_all=avatar_all_serializable, con=con, lib=lib, image_files=image_files, video_files=video_files, image_folder_path=image_folder_path, library_folder_name=library_folder_name, experience_folder_name=experience_folder_name)

# -------------------------------------------------
# creating a post for Switching perspective settings page
@posts.route('/deletavatar', methods=['GET','POST'])
@login_required
def deletavatar():
    name = request.form.get('del_avatar')
    delava = Avatar.query.filter(Avatar.avatar_name==name).first()
    print(name)
    db.session.delete(delava)
    db.session.commit()
    return redirect(request.referrer)


@posts.route('/switchsettings', methods=['GET'])
@login_required
def switchsettings():
    
    text_type = "Switching"
    current_library = request.args.get('library_id', type=int)
    late_ex = request.args.get('experience_id', type=int)

    con = Experience.query.filter_by(eid=late_ex, post_id=current_library)
    lib = Library.query.filter_by(id=current_library)

    current_library = db.session.query(Experience.post_id).filter(
        Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(eid=late_ex, post_id=current_library)
    lib = Library.query.filter_by(id=current_library)
    
    return render_template("switching_settings.html", title='Switching_perspective_Settings', con=con, lib=lib)


@posts.route('/virtualtourlist',methods=['GET', 'POST'])
@login_required
def virtualtourlist():
    current_library = request.args.get('library_id', type=int)
    late_ex = request.args.get('experience_id', type=int)
    optionCount = request.args.get('optionCount', type=int)
    optionCountO = request.args.get('optionCountO', type=int)
    con = Experience.query.filter_by(
        eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    type_current = Conversation.query.filter_by(
        library_id=current_library, experience_id=late_ex).first()
    # type_current=Conversation.query.filter_by(id=current_con)
    current_show = Question_option.query.filter_by(question_id = 16)
    library_folder_name = secure_filename(lib.title)
    experience_folder_name = secure_filename(con.etitle)
    session['library_folder_name'] = library_folder_name
    session['experience_folder_name'] = experience_folder_name
    destination_path_v = session.get('destination_path', None)
    video_folder_path = os.path.join(
        current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
     # ---------------  Video upload and save functions ------------------------------------------
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                # flash('No selected file')
                return redirect(request.url)
            if file and allowed_video(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(video_folder_path, filename))
                uploaded_files.append(filename)
        # flash('Files uploaded successfully')
        # Join the filenames into a comma-separated string
        filenames_string = ','.join(uploaded_files)
    
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    exp_id = session.get('exp_id' , None)
    hotsp=db.session.query(Hotspot).filter(Hotspot.ex_id == late_ex).all()
    current_show = Question_option.query.filter_by(question_id = 16)
    return render_template('virtualtour.html', title='Conversation Page', optionCount=optionCount, optionCountO=optionCountO, con=con, lib=lib, current_question=current_show,video_files=video_files,library_folder_name=library_folder_name, experience_folder_name=experience_folder_name,destination_path_v=destination_path_v,hotsp=hotsp)


@posts.route('/hotspot_video', methods=['GET',"POST"])
@login_required
def hotspot_video():
    late_ex = db.session.query(func.max(Experience.eid)).scalar()
    current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    library_title = secure_filename(lib.title)
    experience_title = secure_filename(con.etitle)
    library_folder_name = secure_filename(lib.title)
    experience_folder_name = secure_filename(con.etitle)
    session['library_folder_name'] = library_folder_name
    session['experience_folder_name'] = experience_folder_name
    exp_id= request.form.get('exp_id',type=int)
    name = request.form.get('hotspotText', type=str)
    time = request.form.get("timeup", default=1.72, type=float)
    x=request.form.get('x', type=str)
    y=request.form.get('y', type=str)
    video_folder_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
    video_files = get_videos(video_folder_path)
    session['video_files'] = video_files
    print('time:', time)
    print("X :",x)
    return render_template("hotspot_video.html", name=name, currentTime=time,video_files=video_files,library_folder_name=library_folder_name, experience_folder_name=experience_folder_name,x=x,y=y,exp_id=exp_id)


@posts.route('/test', methods=['GET'])
@login_required
def test():
    try:
        # Construct the full path to the target directory
        target_path = os.path.join(
            current_app.root_path, 'static', 'for_CHECK')
        # Create the directory
        os.mkdir(target_path)
    except FileExistsError:
        print("Folder 'for_CHECK' already exists.")
    return render_template("home.html")


@posts.route('/testpage', methods=['GET'])
@login_required
def testpage():
    late_ex = db.session.query(func.max(Experience.eid)).scalar()
    current_library = db.session.query(Experience.post_id).filter(
        Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(
        eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    library_title = secure_filename(lib.title)
    experience_title = secure_filename(con.etitle)
    return render_template("test.html", lib=lib, experience_title=experience_title, library_title=library_title, con=con)


@posts.route('/save_selected', methods=['POST'])
def save_selected():
    late_ex = db.session.query(func.max(Experience.eid)).scalar()
    current_library = db.session.query(Experience.post_id).filter(
    Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    library_title = secure_filename(lib.title)
    experience_title = secure_filename(con.etitle)
    library_folder_name = secure_filename(lib.title)
    experience_folder_name = secure_filename(con.etitle)
    session['library_folder_name'] = library_folder_name
    session['experience_folder_name'] = experience_folder_name
    # Handle saving files to selected_images folder
    for key in request.files:
        file = request.files[key]
        filename = secure_filename(file.filename)  # Secure the filename
        file.save(os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "selected_images", filename))

    # Return a response if needed
    return 'Images saved successfully'

@posts.route('/upload', methods=['POST'])
def upload():
    # Handle file uploads here (if needed)
    return 'Files uploaded successfully'


import time

import shutil  # Add this import at the beginning of your file

@posts.route('/save_video', methods=['POST'])
def save_video():
    late_ex = db.session.query(func.max(Experience.eid)).scalar()
    current_library = db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
    con = Experience.query.filter_by(eid=late_ex, post_id=current_library).first()
    lib = Library.query.filter_by(id=current_library).first()
    library_folder_name = secure_filename(lib.title)
    experience_folder_name = secure_filename(con.etitle)
    session['library_folder_name'] = library_folder_name
    session['experience_folder_name'] = experience_folder_name
    data = request.get_json()
    filename = data['filename']
    source_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video", filename)
    destination_path =os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "selected_video", filename)
    session['filename_vv'] = "./static/Library/"+library_folder_name+"/"+experience_folder_name+"/selected_video/"+filename
    

    # Ensure directories exist
    temp_videos_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "temp_video")
    selected_videos_path = os.path.join(current_app.root_path, 'static', "Library", library_folder_name, experience_folder_name, "selected_video")
    

    os.makedirs(temp_videos_path, exist_ok=True)
    os.makedirs(selected_videos_path, exist_ok=True)

    current_app.logger.info(f'Source path: {source_path}')
    current_app.logger.info(f'Destination path: {destination_path}')
    try:
        if os.path.exists(source_path):
            time.sleep(0.1)  # Add a short delay before copying the file
            shutil.copy(source_path, destination_path)  # Use shutil.copy() instead of os.rename()
            return 'Video saved successfully'
        else:
            return 'Source file does not exist'
    except Exception as e:
        return 'Error: ' + str(e)
    





ch=0
@posts.route('/update_tree', methods=['POST'])
def update_tree():
    global ch
    late_ex = db.session.query(func.max(Experience.eid)).scalar()
    root_node = Node.query.filter_by(id=1, ex_id=late_ex).first()
    try:
        data = request.json
        from flask import current_app

        current_app.logger.info("Received data for saving tree: %s", data)

        if 'nodes' not in data:
            raise ValueError("Invalid data format. 'nodes' key not found.")

        nodes_to_insert = []
        nodes_to_update = []
        
        for node_data in data['nodes']:
            node_name = node_data.get('name')
            parent_id = int(node_data.get('parent_id')) if node_data.get('parent_id') is not None else None
            late_ex = db.session.query(func.max(Experience.eid)).scalar()
            node = Node.query.filter_by(ex_id=late_ex).filter_by(name=node_name).first()
            if not root_node:
                root_node = Node(parent_id=None, name="root", ex_id=late_ex)
                db.session.add(root_node)
            if node:
                if node.id != 1:
                    node.parent_id = parent_id
                    node.name = node_name
                nodes_to_update.append(node)
            else:
                if parent_id == 0:
                    # Handle root node creation separately if needed
                    parent_id = 1  # Default to root node if no parent specified
                    node = Node(parent_id=parent_id, name=node_name,ex_id=late_ex)
                    nodes_to_insert.append(node)
                else:
                    if ch ==0:
                        node = Node(parent_id=parent_id+1, name=node_name,ex_id=late_ex)
                        nodes_to_insert.append(node)
                    else:
                        node = Node(parent_id=parent_id, name=node_name,ex_id=late_ex)
                        nodes_to_insert.append(node)

        if nodes_to_insert:
            # Check if root node exists, create if not
            root_node = Node.query.filter_by(id=1).first() 
            if not root_node:
                ch=0
                root_node = Node(id=1, parent_id=None, name="root",ex_id=late_ex)
                db.session.add(root_node)
                db.session.commit()

            db.session.add_all(nodes_to_insert)

        for node in nodes_to_update:
            if node.id == 1:  # Skip the update for the root node
                continue
            db.session.add(node)

        db.session.commit()
        
        ch=ch+1
        current_app.logger.info("Tree saved successfully")
        return jsonify({'message': 'Tree saved successfully'})
    except Exception as e:
        current_app.logger.error("Error saving tree: %s", str(e))
        db.session.rollback()
        return jsonify({'error': 'An error occurred while saving the tree'}), 500


@posts.route('/get_tree_data', methods=['GET'])
def get_tree_data():
    try:
        late_ex = db.session.query(func.max(Experience.eid)).scalar()
        
        # Filter nodes where ex_id equals late_ex
        nodes = Node.query.filter(Node.ex_id == late_ex).all()
        tree_data = [{'id': str(node.id), 'parent_id': str(node.parent_id), 'name': node.name} for node in nodes]
        return jsonify({'nodes': tree_data})
    except Exception as e:
        posts.logger.error("Error fetching tree data: %s", str(e))
        return jsonify({'error': 'An error occurred while fetching tree data'}), 500