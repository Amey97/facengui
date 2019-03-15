var train_data = {
    name: "",
    contact: "",
    file: null,
    contact: "",
    address: "",
    aadhar: "",
    crime: "",
    act: "",
    gender: "",
    dob: ""
};

var recognize_data = {
    file: null
};


var message = null;
var active_section = null;

function render(){

   // clear form data

   $('.form-item input').val('');
   $('.tabs li').removeClass('active');
   $('.tabs li:first').addClass('active');


   active_section = 'train-content';

    $('#'+active_section).show();


}
function update(){


    if(message){
        // render message

        $('.message').html('<p class="'+_.get(message, 'type')+'">'+_.get(message, 'message')+'</p>');
    }else{
        $('.message').html('');
    }

    $('#train-content, #recognize-content').hide();
    $('#'+active_section).show();



}


$(document).ready(function(){




    // listen for file added

    $('#train #input-file').on('change', function(event){



        //set file object to train_data
        train_data.file = _.get(event, 'target.files[0]', null);


    });


    // listen for name change
    $('#name-field').on('change', function(event){

        train_data.name = _.get(event, 'target.value', '');

    });

    $('#contact-field').on('change', function(event){

        train_data.contact = _.get(event, 'target.value', '');

    });


    $('#address-field').on('change', function(event){

        train_data.address = _.get(event, 'target.value', '');

    });

    $('#aadhar-field').on('change', function(event){

        train_data.aadhar = _.get(event, 'target.value', '');

    });

    $('#crime-field').on('change', function(event){

        train_data.crime = _.get(event, 'target.value', '');

    });

    $('#act-field').on('change', function(event){

        train_data.act = _.get(event, 'target.value', '');

    });

    $('#gender-field').on('change', function(event){

        train_data.gender = _.get(event, 'target.value', '');

    });

    $('#dob-field').on('change', function(event){

        train_data.dob = _.get(event, 'target.value', '');

    });


    // listen tab item click on

    $('.tabs li').on('click', function(e){

        var $this = $(this);


        active_section = $this.data('section');

        // remove all active class

        $('.tabs li').removeClass('active');

        $this.addClass('active');

        message = null;

        update();



    });


    // listen the form train submit

    $('#train').submit(function(event){

        message = null;

        if(train_data.name && train_data.file || train_data.contact ){
            // do send data to backend api

            var train_form_data = new FormData();

            train_form_data.append('name', train_data.name);
            train_form_data.append('contact', train_data.contact);
            train_form_data.append('address', train_data.address);
            train_form_data.append('aadhar', train_data.aadhar);
            train_form_data.append('crime', train_data.crime);
            train_form_data.append('act', train_data.act);
            train_form_data.append('gender', train_data.gender);
            train_form_data.append('dob', train_data.dob);
            train_form_data.append('file', train_data.file);


            axios.post('/api/train', train_form_data).then(function(response){

                message = {type: 'success', message: 'Record has been added.: ' + _.get(response, 'data.id')};

                train_data = {name: '',contact:'',address:'', aadhar:'',crime:'',act:'',gender:'', dob:'', file: null};
                update();

            }).catch(function(error){


                  message = {type: 'error', message: _.get(error, 'response.data.error.message', 'Unknown error.')}

                  update();
            });

        }else{

            message = {type: "error", message: "Name and face image is required."}



        }

        update();
        event.preventDefault();
    });


    // listen for recognize file field change
    $('#recognize-input-file').on('change', function(e){


        recognize_data.file = _.get(e, 'target.files[0]', null);

    });
    // listen for recognition form submit
    $('#recognize').submit(function(e){



        // call to backend
        var recog_form_data = new FormData();
        recog_form_data.append('file', recognize_data.file);

        axios.post('/api/recognize', recog_form_data).then(function(response){


            console.log("We found a user matched with your face image is", response.data);

            message = {type: 'success', message: 'Name of Criminal: '+ response.data.user.name};

            recognize_data = {file: null};
            update();

        }).catch(function(err){


            message = {type: 'error', message: _.get(err, 'response.data.error.message', 'Unknown error')};

            update();

        });
        e.preventDefault();
    });




// render the app;
render();

});



