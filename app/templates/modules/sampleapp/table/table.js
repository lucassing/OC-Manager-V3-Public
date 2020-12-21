const OPTIONS = ["Water", "Methanol", "Acetone", "Specific"]

class Table {
    row = [];

    constructor(number_of_rows, calculationMethod) {
        this.numberOfRows = 0;
        this.calculationMethod = calculationMethod;
        this.#addMultipleRows(number_of_rows);
    }

    destructor(){
        for(let i=this.numberOfRows-1; i>=0;i--){
            this.row[i].eliminate()
            this.row.pop()
            this.numberOfRows--;
        }
    }

    #addRow(){
        /**
         * Appends a row at the end of #tbody-band
         * @param  {void}
         * @return  {Object<tr.band-row>}
         */
        this.numberOfRows = this.row.push(new Table.#Row(this.calculationMethod))
        return this.row[this.numberOfRows-1];
    }

    #addMultipleRows(n){
        /**
         * Create n number of rows
         * @param  {number}
         * @return  {void}
         */
        for(let i=1; i<=n;i++){
            let newRow = this.#addRow();
            newRow.setBandNumber(this.numberOfRows)
        }
    }

    ///ERROR DEVOLVER EL OBJETO
    getRowByNumber(numberOfRow){
        /**
         * Returns the row object selected by number of row
         * @param  {Number}
         * @return  {Object<tr.band-row>}
         */
        let row = $('.band-number').filter(function(){
            return this.innerHTML == numberOfRow
        }).parent();
        return row
    }

    getTableValues(){
        let data = [];
        if(this.numberOfRows==0){
            console.log("Empty table")
            return
        }
        else{
            this.row.forEach(function (value){
                data.push(value.getRowData())
            })
        }
        return data
    }

    setTableCalculationValues(data){
        data.forEach(function(row,index,array){
            this.row[index].setCalculatedData(row)
        },this)
    }

    loadTable(data){
        data.forEach(function(data,index,array){
            this.row[index].loadDataInRow(data)
        },this)
    }

    static #Row = class Row{
        row = null;

        constructor(calculationMethod){
            this.row = $(".band-row").first().clone().show().appendTo("#tbody-band");
            this.solventOptions = OPTIONS;
            this.#setSolventOptions();
            this.calculationMethod = calculationMethod
            this.setCalculateMethod();
        }

        setCalculateMethod(){
            this.row.find('.volume, .solvent_select').on("change",this.calculationMethod)
        }

        setEstimatedVolume(value){
            this.row.find('.estimated-volume').text(value.toFixed(3))
        }

        getEstimatedVolume(){
            let value = this.row.find('.estimated-volume').text()
            return this.#sanityUndefined(value)
        }

        setEstimatedDropVolume(value){
            this.row.find('.estimated-drop').text(value.toFixed(3))
        }
        getEstimatedDropVolume(){
            let value = this.row.find('.estimated-drop').text()
            return this.#sanityUndefined(value)
        }


        setMinimumVolume(value){
            this.row.find('.minimum-volume').text(value.toFixed(3))
        }
        getMinimumVolume(){
            let value = this.row.find('.minimum-volume').text()
            return this.#sanityUndefined(value)
        }

        setSolventOption(value){
            this.row.find('.solvent_select').val(value)
        }
        getSolventOption(){
            let value = this.row.find('.solvent_select').val()
            return this.#sanityUndefined(value)
        }

        setDescription(value){
            this.row.find('.description-column').text(value)
        }
        getDescription(){
            let value = this.row.find('.description-column').text()
            return this.#sanityUndefined(value)
        }

        setVolumeValue(value){
            this.row.find('.volume').val(value)
        }
        getVolumeValue(){
            let value = this.row.find('.volume').val()
            return this.#sanityUndefined(value)
        }

        setBandNumber(value){
            this.row.find('.band-number').text(value)
        }
        getBandNumber(){
            let value = this.row.find('.band-number').text()
            return this.#sanityUndefined(value)
        }

        setViscosity(value){
            this.row.find('.viscosity').text(value)
        }
        getViscosity(){
            let value = this.row.find('.viscosity').text()
            return this.#sanityUndefined(value)
        }

        setDensity(value){
            this.row.find('.density').text(value)
        }
        getDensity(){
            let value = this.row.find('.density').text()
            return this.#sanityUndefined(value)
        }



        #setSolventOptions(){
            /**
             * adds the solvents options to a cell
             * @param  {Object<tr.band-row> , options list}
             * @return  {void}
             */
            for(let option in this.solventOptions){
                let aux = this.row.find('option:first')
                aux.clone()
                    .show()
                    .attr("value",this.solventOptions[option])
                    .text(this.solventOptions[option])
                    .appendTo(aux.parent())
            }
            this.row.find('select').val(this.solventOptions[0])
            this.row.find('select').on("change",function (){
                if($(this).val()=="Specific"){
                    $(this).closest('.band-row').find('.specific-options').fadeIn()
                }
                else{
                    $(this).closest('.band-row').find('.specific-options').fadeOut()
                }
            })
        }

        #sanityUndefined(value){
            if(value==undefined){
                value = "";
            }
            return value;
        }

        getRowData(){
            let data = {
                "band_number": this.getBandNumber(),
                "description": this.getDescription(),
                "volume": this.getVolumeValue(),
                "type": this.getSolventOption(),
                "density": this.getDensity(),
                "viscosity": this.getViscosity(),
                "estimated_volume": this.getEstimatedVolume(),
                "estimated_drop_volume": this.getEstimatedDropVolume(),
                "minimum_volume": this.getMinimumVolume()
            }
            return data
        }

        setCalculatedData(data){
            this.setEstimatedDropVolume(data.estimated_drop_volume)
            this.setMinimumVolume(data.minimum_volume)
            this.setEstimatedVolume(data.estimated_volume)
        }

        loadDataInRow(data){
            this.setBandNumber(data.band_number)
            this.setDescription(data.description)
            this.setVolumeValue(data.volume)
            this.setSolventOption(data.type)
            this.setDensity(data.density)
            this.setViscosity(data.viscosity)
        }

        eliminate(){
            this.row.remove();
        }
    }
}


