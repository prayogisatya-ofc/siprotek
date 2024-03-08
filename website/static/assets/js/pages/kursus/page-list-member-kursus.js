Vue.createApp({
    data() {
        return {
            search: '',
            division: '',
            datas: [],
            csrf: token,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.initializeSelect2()
        this.getDatas()
    },
    methods: {
        initializeSelect2(){
            var select2 = $('.select2')
            if (select2.length) {
                select2.each(function () {
                    var $this = $(this);
                    $this.wrap('<div class="position-relative"></div>').select2({
                        dropdownParent: $this.parent(),
                        placeholder: $this.data('placeholder')
                    })
                })
            }
            $('.select2').on('change', (event) => {
                this.division = event.target.value
                this.getDatas()
            })
        },
        async getDatas(){
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

            await axios.get(`/all-courses/get-data?search=${this.search}&division=${this.division}`)
                .then((result) => {
                    $.unblockUI();

                    var data = JSON.parse(result.data)
                    this.datas = data.data
                    this.pagination = data.pagination
                })
                .catch(() => {
                    $.unblockUI();
                    
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        }
    }
}).mount('#app')