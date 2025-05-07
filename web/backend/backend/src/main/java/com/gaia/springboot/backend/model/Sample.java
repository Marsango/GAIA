package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "sample")
public class Sample {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "description")
    private String description;

    @Column(name = "sample_number")
    private Integer sampleNumber;

    @Column(name = "collection_date")
    private String collectionDate;

    @Column(name = "total_area")
    private Double totalArea;

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "smp")
    private Double smp;

    @Column(name = "depth")
    private Double depth;

    @Column(name = "phosphorus")
    private Double phosphorus;

    @Column(name = "potassium")
    private Double potassium;

    @Column(name = "organic_matter")
    private Double organicMatter;

    @Column(name = "ph")
    private Double ph;

    @Column(name = "aluminum")
    private Double aluminum;

    @Column(name = "h_al")
    private Double hAl;

    @Column(name = "calcium")
    private Double calcium;

    @Column(name = "magnesium")
    private Double magnesium;

    @Column(name = "copper")
    private Double copper;

    @Column(name = "iron")
    private Double iron;

    @Column(name = "manganese")
    private Double manganese;

    @Column(name = "zinc")
    private Double zinc;

    @Column(name = "base_sum")
    private Double baseSum;

    @Column(name = "clay")
    private Double clay;

    @Column(name = "silte")
    private Double silte;

    @Column(name = "classification")
    private String classification;

    @Column(name = "sand")
    private Double sand;

    @Column(name = "ctc")
    private Double ctc;

    @Column(name = "v_percent")
    private Double vPercent;

    @Column(name = "aluminum_saturation")
    private Double aluminumSaturation;

    @Column(name = "effective_ctc")
    private Double effectiveCtc;

    @Column(name = "used_config")
    private String usedConfig;

    @ManyToOne
    @JoinColumn(name = "fk_property_id")
    private Property property;

    public Sample(){

    }

    public Double getSilte() {
        return silte;
    }

    public void setSilte(Double silte) {
        this.silte = silte;
    }

    public Property getProperty() {
        return property;
    }


    public String getUsedConfig() {
        return usedConfig;
    }

    public void setUsedConfig(String usedConfig) {
        this.usedConfig = usedConfig;
    }

    public Double getEffectiveCtc() {
        return effectiveCtc;
    }

    public void setEffectiveCtc(Double effectiveCtc) {
        this.effectiveCtc = effectiveCtc;
    }

    public Double getAluminumSaturation() {
        return aluminumSaturation;
    }

    public void setAluminumSaturation(Double aluminumSaturation) {
        this.aluminumSaturation = aluminumSaturation;
    }

    public Double getvPercent() {
        return vPercent;
    }

    public void setvPercent(Double vPercent) {
        this.vPercent = vPercent;
    }

    public Double getCtc() {
        return ctc;
    }

    public void setCtc(Double ctc) {
        this.ctc = ctc;
    }

    public Double getSand() {
        return sand;
    }

    public void setSand(Double sand) {
        this.sand = sand;
    }

    public String getClassification() {
        return classification;
    }

    public void setClassification(String classification) {
        this.classification = classification;
    }

    public Double getClay() {
        return clay;
    }

    public void setClay(Double clay) {
        this.clay = clay;
    }

    public Double getBaseSum() {
        return baseSum;
    }

    public void setBaseSum(Double baseSum) {
        this.baseSum = baseSum;
    }

    public Double getZinc() {
        return zinc;
    }

    public void setZinc(Double zinc) {
        this.zinc = zinc;
    }

    public Double getManganese() {
        return manganese;
    }

    public void setManganese(Double manganese) {
        this.manganese = manganese;
    }

    public Double getIron() {
        return iron;
    }

    public void setIron(Double iron) {
        this.iron = iron;
    }

    public Double getCopper() {
        return copper;
    }

    public void setCopper(Double copper) {
        this.copper = copper;
    }

    public Double getMagnesium() {
        return magnesium;
    }

    public void setMagnesium(Double magnesium) {
        this.magnesium = magnesium;
    }

    public Double getCalcium() {
        return calcium;
    }

    public void setCalcium(Double calcium) {
        this.calcium = calcium;
    }

    public Double gethAl() {
        return hAl;
    }

    public void sethAl(Double hAl) {
        this.hAl = hAl;
    }

    public Double getAluminum() {
        return aluminum;
    }

    public void setAluminum(Double aluminum) {
        this.aluminum = aluminum;
    }

    public Double getPh() {
        return ph;
    }

    public void setPh(Double ph) {
        this.ph = ph;
    }

    public Double getOrganicMatter() {
        return organicMatter;
    }

    public void setOrganicMatter(Double organicMatter) {
        this.organicMatter = organicMatter;
    }

    public Double getPotassium() {
        return potassium;
    }

    public void setPotassium(Double potassium) {
        this.potassium = potassium;
    }

    public Double getPhosphorus() {
        return phosphorus;
    }

    public void setPhosphorus(Double phosphorus) {
        this.phosphorus = phosphorus;
    }

    public Double getDepth() {
        return depth;
    }

    public void setDepth(Double depth) {
        this.depth = depth;
    }

    public Double getSmp() {
        return smp;
    }

    public void setSmp(Double smp) {
        this.smp = smp;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getTotalArea() {
        return totalArea;
    }

    public void setTotalArea(Double totalArea) {
        this.totalArea = totalArea;
    }

    public String getCollectionDate() {
        return collectionDate;
    }

    public void setCollectionDate(String collectionDate) {
        this.collectionDate = collectionDate;
    }

    public Integer getSampleNumber() {
        return sampleNumber;
    }

    public void setSampleNumber(Integer sampleNumber) {
        this.sampleNumber = sampleNumber;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
