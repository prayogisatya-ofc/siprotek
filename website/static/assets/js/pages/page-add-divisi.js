Vue.createApp({
    data() {
        return {
            forms: [{name: null, tutor: null}],
            csrf: token,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.select2Initial()
    },
    methods: {
        select2Initial(){
            var select2 = $('.select2')
            if (select2.length) {
                select2.each((index, element) => {
                    var $this = $(element);
                    $this.wrap('<div class="position-relative"></div>').select2({
                        dropdownParent: $this.parent(),
                        placeholder: $this.data('placeholder')
                    })
                })
                $(document).on('change', '.select2', (event) => {
                    const selectedValue = event.target.value;
                    const select2Index = Array.from($('.select2')).indexOf(event.target);
                    const formIndex = Math.floor(select2Index / 2); // Membagi dua karena setiap form terdiri dari elemen select2 dan div
                    this.forms[formIndex].tutor = selectedValue;
                });
            }
        },
        addForm(){
            this.forms.push({name: null, tutor: null})
            this.$nextTick(() => {
                this.select2Initial()
            })
        },
        removeForm(index) {
            this.forms.splice(index, 1);
        },
        async onSubmit(){
            if(this.forms.length == 0){
                Swal.fire({
                    icon: "warning",
                    text: "Masukkan dulu datanya!",
                    timer: 2000,
                    showConfirmButton: false,
                })
            } else {
                $.blockUI({
                    message: '<div class="spinner-border text-white" role="status"></div>',
                    css: {
                      backgroundColor: 'transparent',
                      border: '0'
                    },
                    overlayCSS: {
                      opacity: 0.5
                    }
                })
    
                await axios.post('/divisions/add/submit', this.forms, { 
                    headers: { "X-CSRFToken": this.csrf }
                })
                .then(response => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "success",
                        text: response.data.success,
                        timer: 2000,
                        showConfirmButton: false,
                    }).then(() => {
                        location.href = "/divisions"
                    })
                })
                .catch(error => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "error",
                        text: error.response.data.error,
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
            }
        }
    }
}).mount('#app')