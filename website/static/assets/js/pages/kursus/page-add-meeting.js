Vue.createApp({
    data() {
        return {
            form: {
                title: null,
                video: null,
                material: '',
            },
            uuid: null,
            editor: null,
            csrf: token
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.uuid = urlPats[urlPats.length - 2]

        this.quillInitial()
    },
    methods: {
        quillInitial(){
            this.editor = new Quill('#snow-editor', {
                bounds: '#snow-editor',
                placeholder: 'Tulis materi nya di sini yaa..',
                modules: {
                  formula: true,
                  toolbar: '#snow-toolbar'
                },
                theme: 'snow'
            })
            this.editor.on('text-change', () => {
                this.form.material = this.editor.root.innerHTML
            });
        },
        async onSubmit(){
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

            await axios.post(`/courses/${this.uuid}/add/submit`, this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    location.href = `/courses/${this.uuid}`
                })
            })
            .catch(error => {
                $.unblockUI()
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        }
    }
}).mount('#app')